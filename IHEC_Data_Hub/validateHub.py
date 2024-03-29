from __future__ import print_function
import jsonschema
from sys import argv, _getframe
import json
import os
import getopt
import re
import logging
import urllib.request
from urllib.error import HTTPError
import requests
from ontology_lookup import OntologyLookup


def main(argv):
    """ Command line way to valide a data hub. """

    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    opts, args = getopt.getopt(argv, "", ["json=", "version=", "loose-validation", "verbose", "epirr"])

    json_filename = ''
    is_loose_validation = False
    validate_epirr = False
    version = '1.0'

    for opt, arg in opts:
        if opt == '--json':
            json_filename = arg
        elif opt == '--version':
            version = arg
        elif opt == '--loose-validation':
            is_loose_validation = True
        elif opt == '--verbose':
            logging.getLogger().setLevel(logging.DEBUG)
        elif opt == '--epirr':
            validate_epirr = True

    # JSON to be validated is mandatory, otherwise, display options
    if json_filename == '':
        printHelp()
        exit()

    schema_file = os.path.dirname(os.path.realpath(__file__)) + '/../schemas/json/' + version + '/hub.json'
    print(schema_file)	
    with open(json_filename) as json_file:
        jsonObj = json.load(json_file)

    try:

        validateJson(jsonObj, schema_file, validate_epirr, is_loose_validation)

        print("Data hub is valid.")

    except jsonschema.exceptions.ValidationError:
        return jsonschemaErrorReport(jsonObj, version)


def jsonschemaErrorReport(jsonObj, schema_version):
    """ Return error report. """

    schema_file = os.path.dirname(os.path.realpath(__file__)) + '/../schemas/json/' + schema_version + '/hub.json'

    with open(schema_file) as jsonStr:
        json_schema = json.load(jsonStr)
    v = jsonschema.Draft7Validator(json_schema, format_checker=jsonschema.FormatChecker())
    errors = [e for e in v.iter_errors(jsonObj)]
    logging.getLogger().info('Total errors: {}'.format(len(errors)))
    print("--------------------------------------------------")
    for error in sorted(errors, key=str):
        logging.getLogger().error('Validation error in {}: {}'.format('.'.join(str(v) for v in error.path),
                                                                      error.message))
        if len(error.context) > 0:
            logging.getLogger().info('Multiple sub-schemas can apply. This is the errors for each:')
            prev_schema = -1
            for suberror in sorted(error.context, key=lambda e: e.schema_path):
                schema_index = suberror.schema_path[0]
                if prev_schema < schema_index:
                    logging.getLogger().info('Schema {}:'.format(schema_index + 1))
                    prev_schema = schema_index
                logging.getLogger().error('{}'.format(suberror.message))
        print("--------------------------------------------------")


def printHelp():
    print("Usage: python validateHub.py --json=doc.json [--version --loose-validation --verbose --epirr]")


def validateJson(jsonObj, schema_file, validate_epirr, is_loose_validation):
    """ Validate a data hub against the IHEC Data Hub Schema. """

    # Syntactic validation
    logging.getLogger().info('Validating syntax against JSON Schema...')
    with open(schema_file) as jsonStr:
        json_schema = json.load(jsonStr)
    jsonschema.validate(jsonObj, json_schema, format_checker=jsonschema.FormatChecker())
    logging.getLogger().info('Schema validation OK.')

    # Semantic validation
    logging.getLogger().info('Validating Datasets object...')
    sample_list = jsonObj['samples'].keys()
    validateDatasets(jsonObj['datasets'], sample_list, is_loose_validation)
    logging.getLogger().info('Datasets validation passed.')

    # EpiRR validation
    if validate_epirr:
        logging.getLogger().info('Validating metadata against EpiRR records...')
        validateEpirr(jsonObj)
        logging.getLogger().info('EpiRR validation finished.')

    # TF Target validation against HGNC
    datasets = jsonObj.get('datasets')
    for dataset_name in datasets:
        dataset = datasets.get(dataset_name)
        experiment_attr = dataset.get('experiment_attributes')
        if experiment_attr.get('experiment_type') == 'Transcription Factor':
            validateHgncSymbol(dataset, dataset_name)

    # get schema version
    schema_version = schema_file.split('/hub.json')[0].split('json/')[1]
    # run ontologies validation if v2.0 since it ontology validation works only for the CURIEs and v1.0 allows URIs
    if schema_version == "2.0":
        validateOntologies(jsonObj)


def validateDatasets(datasets, sample_list, is_loose_validation):
    """ Validate that dataset objects properties are OK. """

    for dn in datasets:
        dataset = datasets[dn]

        # Does the sample name exist in the 'samples' dictionary?
        try:
            if isinstance(dataset['sample_id'], list):
                for sample_id in dataset['sample_id']:
                    if sample_id not in sample_list:
                        raise Exception(sample_id)
            else:
                if dataset['sample_id'] not in sample_list:
                    raise Exception(dataset['sample_id'])
        except Exception as e:
            logging.getLogger().error('Dataset is linked to an unknown sample_id. (sample_id="%s" does not exist in "samples" dictionary).' % (e))

        for track_type in dataset['browser']:

            # Display warning if tracks are of an unknown type, in strict validation mode.
            if not is_loose_validation:
                if track_type not in ["signal_unstranded", "signal_forward", "signal_reverse", "peak_calls", "methylation_profile", "contigs"]:
                    logging.getLogger().error('Track type is not in known types: "%s"' % (track_type))

            try:
                tracks = dataset['browser'][track_type]

                validatePrimaryTrack(tracks)

                for track in tracks:
                    validateMd5(track['md5sum'])

            except Exception as e:
                raise Exception('Problem in dataset "%s" and track type "%s": %s' % (dn, track_type, e))


def validateMd5(md5):
    """ Verify length and character content for provided MD5 checksum. """

    m = re.search('^[0-9abcdefABCDEF]{32}$', md5)
    try:
        m.group(0)
    except:
        raise Exception('Problem with md5sum %s' % (md5))


def validatePrimaryTrack(tracks):
    """ If more than one track is provided for a track type,
    make sure the primary flag is defined, and set to one and only one track. """

    if len(tracks) > 1:
        primary_met = False
        for track in tracks:

            # "primary" property is mandatory when there's more than one track for this type.
            if not 'primary' in track:
                raise Exception('Missing "primary" property.')

            # Only one track should be set as "primary"
            if track['primary']:
                if primary_met:
                    raise Exception('Already met a "primary" track for this track type.')
                primary_met = True

        # One of the track has to be "primary"
        if not primary_met:
            raise Exception('No track defined as "primary: true" for this track type.')


def api_call_epirr(epirr_id):
    """ Call EpiRR api to check if EpiRR record exists. """
    try:
        base_url = 'http://www.ebi.ac.uk/vg/epirr/view/'
        r = requests.get(base_url + epirr_id, headers={'accept': 'application/json'})
        r.raise_for_status()
        response = json.loads(r.content.decode('utf-8'))
        return response

    except requests.exceptions.HTTPError as e:
        logging.getLogger().warning("The record {} is not found ({})".format(epirr_id, e))


# cache EpiRR response to avoid redundant calls
cache = dict()


def api_with_cache(epirr_id):
    """ Cache EpiRR response in cache dict. """
    if epirr_id not in cache:
        cache[epirr_id] = api_call_epirr(epirr_id)
    return cache[epirr_id]


def validateEpirr(jsonObj):
    """ Ensure that IHEC Data Hub metadata matches with EpiRR record. """

    print()

    datasets = jsonObj['datasets']
    samples = jsonObj['samples']

    for dataset_name in datasets:
        dataset = datasets[dataset_name]
        exp_attr = dataset['experiment_attributes']
        # when there is no 'experiment_type' use 'experiment_ontology_uri'
        if exp_attr.get('experiment_type'):
            exp_name = exp_attr.get('experiment_type')[0]
        else:
            exp_name = exp_attr.get('experiment_ontology_uri')[0]

        if isinstance(dataset['sample_id'], list):
            ds_names = dataset['sample_id']
        else:
            ds_names = [dataset['sample_id']]

        # If dataset has an EpiRR id, validate that metadata matches
        if 'reference_registry_id' in exp_attr:
            epirr_id = exp_attr['reference_registry_id'][0]
            logging.getLogger().info('Validating dataset "%s" against EpiRR record "%s"...' % (dataset_name, epirr_id))

            epirr_json = api_with_cache(epirr_id)
            if epirr_json:
                epirr_sample_metadata = epirr_json['meta_data']

                # Validate that each sample that this dataset refers to holds the correct metadata
                for ds_name in ds_names:
                    hub_sample_metadata = samples[ds_name]
                    logging.getLogger().debug('Validating sample "%s" properties...' % (ds_name))
                    validateSample(epirr_sample_metadata, hub_sample_metadata, dataset_name)

                # Case-insensitive check that each experiment that has an EpiRR id is actually registered at EpiRR.
                raw_data_per_exp = {rd['experiment_type'].lower(): rd for rd in epirr_json['raw_data']}
                if exp_name.lower() not in raw_data_per_exp:
                    logging.getLogger().error('-Experiment "%s" could not be found in EpiRR record %s.' % (exp_name, epirr_id))

                print()


def validateSample(epirr_sample_metadata, hub_sample_metadata, dataset_name):
    """Validate that IHEC Data Hub sample object has metadata that matches EpiRR record."""

    validateProperty(epirr_sample_metadata, hub_sample_metadata, dataset_name, 'biomaterial_type')

    # Cell Line
    if 'line' in epirr_sample_metadata:
        validateProperty(epirr_sample_metadata, hub_sample_metadata, dataset_name, 'line')
    else:
        validateProperty(epirr_sample_metadata, hub_sample_metadata, dataset_name, 'disease')

        # For non-Cell Line, a donor_id is required
        validateProperty(epirr_sample_metadata, hub_sample_metadata, dataset_name, 'donor_id')

        if 'cell_type' in epirr_sample_metadata:
            # Primary Cell or Primary Cell Culture
            validateProperty(epirr_sample_metadata, hub_sample_metadata, dataset_name, 'cell_type')
        elif 'tissue_type' in epirr_sample_metadata:
            # Primary Tissue
            validateProperty(epirr_sample_metadata, hub_sample_metadata, dataset_name, 'tissue_type')
        else:
            logging.getLogger().error('-Missing metadata in EpiRR record.')


def validateProperty(epirr_metadata, sample_metadata, dataset_name, prop):
    """Case-insensitive comparison for a property between IHEC Data Hub and EpiRR record."""

    if prop not in epirr_metadata:
        logging.getLogger().warning('-Property "%s" is missing in EpiRR record for experiment "%s".' % (prop, dataset_name))
        return

    if prop not in sample_metadata:
        logging.getLogger().warning('-Property "%s" is missing in data hub sample object for experiment "%s".' % (prop, dataset_name))
        return

    if epirr_metadata[prop].lower() != sample_metadata[prop][0].lower():
        logging.getLogger().warning('-Property "%s" mismatch for experiment "%s": "%s" VS "%s"' % (prop, dataset_name, epirr_metadata[prop], sample_metadata[prop]))
        return


def validateHgncSymbol(dataset, dataset_name):
    """ Validate experiment target tf against HGNC when experiment_type is 'Transcription Factor'. """

    func = _getframe().f_code.co_name
    logging.getLogger(func).info('Validating dataset "{}" against HGNC records...'.format(dataset_name))
    tf_target = dataset.get('experiment_attributes').get('experiment_target_tf')
    if tf_target:
        success = 'Symbol validation passed.'
        fail = 'Symbol validation failed.'
        logging.getLogger(func).info('Validating symbol: {}'.format(tf_target))
        status = symbolStatus(status='symbol', symbol=tf_target)
        if status:
            logging.getLogger(func).info(success)
            return True
        else:
            logging.getLogger(func).info('Validating if symbol was approved previously...')
            status = symbolStatus(status='prev_symbol', symbol=tf_target)
            if status:
                logging.getLogger(func).info(success)
                return True
            else:
                logging.getLogger(func).info(fail)
                return False
    else:
        logging.getLogger(func).error('Experiment target tf is not found in metadata.')


def symbolStatus(status, symbol):
    """ Generic function to call HGNC API """

    # HGNC status options: 'symbol', 'prev_symbol'
    try:
        r = urllib.request.Request('http://rest.genenames.org/search/' + status + "/" + symbol,
                                   headers={"Accept": "application/json"})
        response = urllib.request.urlopen(r).read()
        tftarget_json = json.loads(response.decode('utf-8'))
        tftarget_json = tftarget_json.get('response')
        if tftarget_json.get('numFound') > 0:
            return True
        return False

    except HTTPError as e:
        logging.getLogger().warning("Unexpected error: {}".format(e))


def validateOntologies(jsonObj):
    """
    Validate all ontologies used in metadata: handles two cases
    when ontology curies are present in sample and in experiment
    """

    func = _getframe().f_code.co_name
    # SAMPLES
    samples = jsonObj['samples']
    for sample_name in samples:
        sample = samples.get(sample_name)
        for curie in sample['sample_ontology_curie']:
            ontology_term = OntologyLookup(curie)
            logging.getLogger(func).info('Validating "sample_ontology_curie" in {} ...'.format(sample_name))
            val_rules = ontology_term.check_ontology_rules(
                ontology_type='sample_ontology_curie', schema_object=sample_name,
                subparam=sample['biomaterial_type'][0]
            )

            if val_rules:
                ontology_term.validate_term()
    # EXPERIMENTS: two ontology types here - experiment_ontology_curie & molecule_ontology_curie
    # it handles both
    datasets = jsonObj.get('datasets')
    for dataset_name in datasets:
        dataset = datasets.get(dataset_name)
        exp_attr = dataset.get('experiment_attributes')
        for key, value in exp_attr.items():
            # retrieve ontology type
            if 'ontology_curie' in key:
                for curie in exp_attr[key]:
                    ontology_term = OntologyLookup(curie)
                    logging.getLogger(func).info('Validating "{}" in {} ...'.format(key, dataset_name))
                    val_rules = ontology_term.check_ontology_rules(
                        ontology_type=key, schema_object=dataset_name
                    )
                    if val_rules:
                        ontology_term.validate_term()
            else:
                pass


if __name__ == "__main__":
    main(argv[1:])
