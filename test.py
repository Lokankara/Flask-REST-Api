import unittest
from run import run


class TestParaphraseEndpoint(unittest.TestCase):

    def setUp(self):
        self.run = run.test_client()

    def test_paraphrase_endpoint_success(self):
        expected = {
            "paraphrases": [
                {"tree": "(S (NP (DT the) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT the) (NN mat)))))"},
                {"tree": "(S (NP (DT the) (NN mat)) (VP (VBD was) (VP (VBN sat) (PP (IN on) (NP (DT by) (DT the) (NN cat))))))"},
                {"tree": "(S (NP (DT the) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT the) (NN rug)))))"},
                {"tree": "(S (NP (DT the) (NN rug)) (VP (VBD was) (VP (VBN sat) (PP (IN on) (NP (DT by) (DT the) (NN cat))))))"},
                {"tree": "(S (NP (DT the) (NN mat)) (VP (VBD was) (VP (VBN sat) (PP (IN on) (NP (DT by) (DT the) (NN cat))))))"},
                {"tree": "(S (NP (DT the) (NN rug)) (VP (VBD was) (VP (VBN sat) (PP (IN on) (NP (DT by) (DT the) (NN cat))))))"}
            ]
        }
        tree_str = "(S (NP (DT the) (NN cat)) (VP (VBD sat) (PP (IN on) (NP (DT the) (NN mat)))))"
        response = self.run.get(f"/paraphrase?tree={tree_str}&limit=6")
        assert expected == response.json

    def test_paraphrase_endpoint_error(self):
        expected = {"error": "Missing \"tree\" parameter."}
        response = self.run.get("/paraphrase")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json, expected)

if __name__ == '__main__':
    unittest.main()
