import unittest
from flask import Flask
from app import app

class TestParaphraseEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_paraphrase_endpoint_success(self):
        tree_str = "(S (NP (DT The) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT a) (NN mat)))))"
        expected = {"paraphrases": [{"tree": "(S (NP (DT a) (NN mat)) (VP (VBD sat) (PP (IN on) (NP (DT The) (NN cat)))))"}]}
        response = self.app.get(f"/paraphrase?tree={tree_str}&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected)

    def test_paraphrase_endpoint_error(self):
        expected = {"error": "Missing \"tree\" parameter."}
        response = self.app.get("/paraphrase")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, expected)

if __name__ == '__main__':
    unittest.main()
