import requests
import json
import logging


ontology_rules = {
    'sample_ontology_uri': {
        'Cell Line': 'efo',
        'Primary Cell': 'cl',
        'Primary Tissue': 'uberon'
    },
    'experiment_ontology_uri': 'obi',
    'molecule_ontology_uri': 'so',
    'disease_ontology_uri': 'ncim',
    'donor_health_status_ontology_uri': 'ncim'
}


class OntologyLookup(object):
    # base = 'https://www.ebi.ac.uk/ols/api/ontologies/'
    # e.g. https://www.ebi.ac.uk/ols/api/search?q=EFO_0001639&ontology=efo

    def __init__(self, curie):
        self.curie = curie

    def parseCurie(self):
        """
        follows CURIE pattern e.g. uberon:0013540
        """
        url_data = {}
        parsed_url = self.curie.split(':')
        url_data['ontology_name'] = parsed_url[0]
        url_data['curie'] = parsed_url[1]
        return url_data

    def checkOntologyRules(self, sample, bio_type, ontology_uri_type):
        biomaterial_type = sample.get(bio_type)  # e.g. Primary Tissue
        rule = ontology_rules.get(ontology_uri_type).get(biomaterial_type)  # e.g. uberon
        current_ontology = self.parseCurie().get('ontology_name')
        if current_ontology == rule:
            logging.getLogger().info("{} : {}".format(biomaterial_type, current_ontology))
            return True
        else:
            logging.getLogger().error("Terms from Ontology {} are not allowed for {}".format(current_ontology, biomaterial_type))
            return False

    def payload(self):
        q = self.parseCurie().get('ontology_name').upper() + '_' + self.parseCurie().get('curie')
        ontology = self.parseCurie().get('ontology_name')
        return {'q': q, 'ontology': ontology}

    def validateTerm(self):
        base_url = 'https://www.ebi.ac.uk/ols/api/search'
        try:
            r = requests.get(base_url, headers={'accept': 'application/json'}, params=self.payload())
            response = json.loads(r.content.decode('utf-8'))
            response = response.get('response')
            if response.get('numFound') > 0:
                logging.getLogger().info('Term {} is found'.format(self.curie))
                return True
            else:
                logging.getLogger().info('Term is not found')
                return False
        except requests.exceptions.HTTPError as e:
            logging.getLogger().warning("Unexpected error {}".format(e))
