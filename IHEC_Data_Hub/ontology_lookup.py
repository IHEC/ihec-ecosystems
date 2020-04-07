import requests
import json
import logging
logging.getLogger('urllib3').setLevel(logging.WARNING)

ontology_lookup_logger = logging.getLogger('ontology_lookup')

ontology_rules = {
    'sample_ontology_curie': {
        'Cell Line': 'efo',
        'Primary Cell': 'cl',
        'Primary Tissue': 'uberon'
    },
    'experiment_ontology_curie': 'obi',
    'molecule_ontology_curie': 'so',
    # leaving out these two for now
    # 'disease_ontology_curie': 'ncim',
    # 'donor_health_status_ontology_curie': 'ncim'
}


class OntologyLookup(object):
    """
    Class to handle validation of accepted ontologies
    """

    def __init__(self, curie):
        self.curie = curie

    def logger(self, level, msg):
        return ontology_lookup_logger.log(level, msg)

    def parse_curie(self):
        """
        follows CURIE pattern e.g. uberon:0013540
        """
        curie_data = {}
        try:
            parsed_curie = self.curie.split(':')
            curie_data['ontology_name'] = parsed_curie[0]
            curie_data['curie'] = parsed_curie[1]
        # if curie format was not validated
        except Exception as e:
            self.logger(logging.ERROR, 'Error: {}'.format(e))
        return curie_data


    def check_ontology_rules(self, ontology_type, schema_object, subparam=None, msg=None):
        """
        :param ontology_type: E.g. 'sample_ontology_curie', 'molecule_ontology_curie'
        :param schema_object: Schema object where ontology term is located. Needed for an error message.
        :param subparam: Used to handle complex validation when accepted ontology depends on value of another property,
        e.g. if 'biomaterial_type': 'Cell Line' then accepted ontology for 'sample_ontology_curie' is EFO
        :param msg: custom error message is term is not accepted
        :return: True if validation passed. False if not.
        """

        # check what ontology must be applied by rule
        rule_ontology = ontology_rules[ontology_type] # e.g 'so' or {'Cell Line': 'efo'}
        # the given ontology by input
        current_ontology = self.parse_curie()['ontology_name']
        # check if rule is a dict, then unpack rule ontology based on subparam value
        if isinstance(rule_ontology, dict):
            if subparam:
                rule_ontology = rule_ontology[subparam]
            # if rule_ontology is a dict and subparam is None raise an error
            else:
                raise TypeError('Provide subparam value.')

        if current_ontology == rule_ontology:
            return True
        else:
            if not msg:
                self.logger(logging.ERROR, 'Error in {}: ontology {} is not accepted for this {}.'
                                      'The only accepted ontology is {}.'
                                      .format(schema_object, current_ontology.upper(),
                                              ontology_type, rule_ontology.upper()))
            else:
                self.logger(logging.ERROR, msg)

            return False

    def payload(self):
        """
        Payload for GET e.g. q=EFO_0001639&ontology=efo
        :return: Returns params to query according to API spec
        """
        # Note: ontology lookup service's curie is case sensitive

        q = self.parse_curie()['ontology_name'].upper() + '_' + self.parse_curie()['curie']
        ontology = self.parse_curie()['ontology_name']
        return {'q': q, 'ontology': ontology}

    def validate_term(self):
        """
        Calls ontology lookup API to check if curie is valid
        :return: Returns True if response is not empty
        """
        base_url = 'https://www.ebi.ac.uk/ols/api/search'
        try:
            r = requests.get(base_url, headers={'accept': 'application/json'}, params=self.payload())
            response = json.loads(r.content.decode('utf-8'))
            response = response.get('response')
            if response.get('numFound') > 0:
                self.logger(logging.INFO, 'Ontology term {} is valid'.format(self.curie))
                return True
            else:
                self.logger(logging.ERROR, 'Error: Ontology term {} is not found'.format(self.curie))
                return False
        except requests.exceptions.HTTPError as e:
            self.logger(logging.ERROR, 'Unexpected error {}'.format(e))
