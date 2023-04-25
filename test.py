import json
import unittest
from app import app

class ParaphraseTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_missing_tree_parameter(self):
        response = self.client.get('/paraphrase')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Missing "tree" parameter.')

    def test_invalid_tree_string(self):
        response = self.client.get('/paraphrase?tree=invalid')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Invalid tree string.')

    def test_generate_paraphrases(self):
        tree_str = "(S (NP (DT The) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT the) (NN mat)))))"
        response = self.client.get(f'/paraphrase?tree={tree_str}&limit=2')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['paraphrases']), 2)
        self.assertIn('The mat sat on the cat.', [p['tree'] for p in data['paraphrases']])
        self.assertIn('The cat sat on the mat.', [p['tree'] for p in data['paraphrases']])

if __name__ == '__main__':
    unittest.main()
