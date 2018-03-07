from __future__ import print_function
import jsonschema
from sys import argv
import json
import os
import getopt
import re
import logging
import urllib2


def main(argv):
    """Command line way to valide a data hub"""

    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    opts, args = getopt.getopt(argv, "", ["json=", "loose-validation", "verbose", "epirr"])

    json_filename = ''
    is_loose_validation = False
    is_verbose = False
    validate_epirr = False

    for opt, arg in opts:
        if opt == '--json':
            json_filename = arg
        elif opt == '--loose-validation':
            is_loose_validation = True
        elif opt == '--verbose':
            is_verbose = True
            logging.getLogger().setLevel(logging.DEBUG)
        elif opt == '--epirr':
            validate_epirr = True

    #JSON to be validated is mandatory, otherwise, display options
    if json_filename == '':
        printHelp()
        exit()

    schema_file = os.path.dirname(os.path.realpath(__file__)) + '/schema/hub.json'

    with open(json_filename) as json_file:
        jsonObj = json.load(json_file)

    try:
        validateJson(jsonObj, schema_file, validate_epirr, is_loose_validation)

        print("Data hub is valid.")

    except jsonschema.exceptions.ValidationError as e:
        print("--------------------------------------------------")
        print("- Validation error")
        print("--------------------------------------------------")
        if is_verbose:
            print(e)
        else:
            try:
                c = e.context.pop()
                print(c.message)
            except IndexError as ie:
                print(e.message)


def printHelp():
    print("Usage: python validateHub.py --json=doc.json [--loose-validation --verbose --epirr]")


def validateJson(jsonObj, schema_file, validate_epirr, is_loose_validation):
    """Validate a data hub against the IHEC Data Hub Schema"""

    #Syntactic validation
    logging.getLogger().info('Validating syntax against JSON Schema...')
    with open(schema_file) as jsonStr:
        json_schema = json.load(jsonStr)
    jsonschema.validate(jsonObj, json_schema, format_checker=jsonschema.FormatChecker())
    logging.getLogger().info('Schema validation OK.')

    #Semantic validation
    logging.getLogger().info('Validating Datasets object...')
    sample_list = jsonObj['samples'].keys()
    validateDatasets(jsonObj['datasets'], sample_list, is_loose_validation)
    logging.getLogger().info('Datasets validation passed.')

    #EpiRR validation
    if validate_epirr:
        logging.getLogger().info('Validating metadata against EpiRR records...')
        validateEpirr(jsonObj)
        logging.getLogger().info('EpiRR validation passed.')


def validateDatasets(datasets, sample_list, is_loose_validation):
    """Validate that dataset objects properties are OK."""

    for dn in datasets:
        dataset = datasets[dn]

        #Does the sample name exist in the 'samples' dictionary?
        if dataset['sample_id'] not in sample_list:
            logging.getLogger().error('Dataset is linked to an unknown sample_id. (sample_id="%s" does not exist in "samples" dictionary).' % (dataset['sample_id']))

        for track_type in dataset['browser']:

            #Display warning if tracks are of an unknown type, in strict validation mode.
            if not is_loose_validation:
                if track_type not in ["signal_unstranded", "signal_forward", "signal_reverse", "peak_calls", "methylation_profile", "contigs"]:
                    logging.getLogger().error('Track type is not in known types: "%s"' % (track_type))

            try:
                tracks = dataset['browser'][track_type]

                validatePrimaryTrack(tracks)

                for track in tracks:
                    validateMd5(track['md5sum'])

            except Exception as e:
                raise Exception('Problem in dataset "%s" and track type "%s": %s' % (dn, track_type, e.message))


def validateMd5(md5):
    """Verify length and character content for provided MD5 checksum."""

    m = re.search('^[0-9abcdefABCDEF]{32}$', md5)
    try:
        m.group(0)
    except:
        raise Exception('Problem with md5sum %s' % (md5))


def validatePrimaryTrack(tracks):
    """If more than one track is provided for a track type, make sure the primary flag is defined, and set to one and only one track."""

    if len(tracks) > 1:
        primary_met = False
        for track in tracks:

            #"primary" property is mandatory when there's more than one track for this type.
            if not 'primary' in track:
                raise Exception('Missing "primary" property.')

            #Only one track should be set as "primary"
            if track['primary']:
                if primary_met:
                    raise Exception('Already met a "primary" track for this track type.')
                primary_met = True

        #One of the track has to be "primary"
        if not primary_met:
            raise Exception('No track defined as "primary: true" for this track type.')


def validateEpirr(jsonObj):
    """Ensure that IHEC Data Hub metadata matches with EpiRR record."""

    print()

    datasets = jsonObj['datasets']
    samples = jsonObj['samples']

    for dataset_name in datasets:
        dataset = datasets[dataset_name]
        exp_attr = dataset['experiment_attributes']
        exp_name = exp_attr['experiment_type']

        if isinstance(dataset['sample_id'], list):
            ds_names = dataset['sample_id']
        else:
            ds_names = [dataset['sample_id']]

        #If dataset has an EpiRR id, validate that metadata matches
        if 'reference_registry_id' in exp_attr:
            epirr_id = exp_attr['reference_registry_id']
            logging.getLogger().info('Validating dataset "%s" against EpiRR record "%s"...' % (dataset_name, epirr_id))

            try:
                request = urllib2.Request('http://www.ebi.ac.uk/vg/epirr/view/' + epirr_id, headers={"Accept": "application/json"})
                response = urllib2.urlopen(request).read()
            except urllib2.HTTPError as e:
                print('Unexpected error: %s' % (e.message))
                continue

            epirr_json = json.loads(response)
            epirr_sample_metadata = epirr_json['meta_data']

            #Validate that each sample that this dataset refers to holds the correct metadata
            for ds_name in ds_names:
                hub_sample_metadata = samples[ds_name]
                logging.getLogger().debug('Validating sample "%s" properties...' % (ds_name))
                validateSample(epirr_sample_metadata, hub_sample_metadata, dataset_name)

            #Case-insensitive check that each experiment that has an EpiRR id is actually registered at EpiRR.
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

    if epirr_metadata[prop].lower() != sample_metadata[prop].lower():
        logging.getLogger().warning('-Property "%s" mismatch for experiment "%s": "%s" VS "%s"' % (prop, dataset_name, epirr_metadata[prop], sample_metadata[prop]))
        return


if __name__ == "__main__":
    main(argv[1:])