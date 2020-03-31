import unittest
from ontology_lookup import OntologyLookup


class OntologyLookupTestCase(unittest.TestCase):

    def setUp(self) -> None:
        # term is not found
        self.invalid_experiment_term = OntologyLookup('obi:000185812')
        # ontology is not accepted
        self.invalid_ontology_sample = OntologyLookup('obi:0001858')

    def test_ontology_rules(self):
        with self.assertRaises(TypeError):
            self.invalid_experiment_term.check_ontology_rules(ontology_type='sample_ontology_curie',
                                                                    schema_object='experiment')
        self.assertEqual(self.invalid_experiment_term.check_ontology_rules(
            ontology_type='experiment_ontology_curie', schema_object='experiment'), True)
        self.assertEqual(self.invalid_ontology_sample.check_ontology_rules(
            ontology_type='sample_ontology_curie', schema_object='sample', subparam='Cell Line'), False)

    def test_validate_term(self):
        self.assertEqual(self.invalid_experiment_term.validate_term(), False)
        self.assertEqual(self.invalid_ontology_sample.validate_term(), True)


if __name__ == '__main__':
    unittest.main()
