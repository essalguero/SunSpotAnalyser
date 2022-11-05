import unittest
import requests
import json

class TestApp(unittest.TestCase):
    url = 'http://localhost:5000/sun-spot-analyser-api/'

    def setUp(self):
        pass

    def test_info(self):
        resp = requests.get(self.url + 'info')
        self.assertEqual(resp.status_code, 200)

    def test_scores(self):
        resp = requests.get(self.url + 'scores?id=1')
        self.assertEqual(resp.status_code, 200)

    def test_ingest_grid(self):
        new_grid = dict(size=0, values=None)
        resp = requests.post(self.url + 'grid', json=new_grid)
        self.assertEqual(resp.status_code, 500)

        new_grid = dict(size=1, values=None)
        resp = requests.post(self.url + 'grid', json=new_grid)
        self.assertEqual(resp.status_code, 500)

        new_grid = dict(size=2, values='1')
        resp = requests.post(self.url + 'grid', json=new_grid)
        self.assertEqual(resp.status_code, 500)

        new_grid = dict(size=1, values='1')
        resp = requests.post(self.url + 'grid', json=new_grid)
        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.text)
        resp = requests.get(self.url + 'scores?id={0}'.format(resp_dict['id']))
        self.assertEqual(eval(resp.text), {'scores': [{'x': 0, 'y': 0, 'score': 1}]})

        new_grid = dict(size=3, values='4, 2, 3, 2, 2, 1, 3, 2, 1')
        resp = requests.post(self.url + 'grid', json=new_grid)
        self.assertEqual(resp.status_code, 200)
        resp_dict = json.loads(resp.text)
        resp = requests.get(self.url + 'scores?id={0}'.format(resp_dict['id']))

        dict_to_check = dict(scores=[{"score": 10, "x": 0, "y": 0}, {"score": 14, "x": 0, "y": 1},
                                     {"score": 8, "x": 0, "y": 2}, {"score": 15, "x": 1, "y": 0},
                                     {"score": 20, "x": 1, "y": 1}, {"score": 11, "x": 1, "y": 2},
                                     {"score": 9, "x": 2, "y": 0}, {"score": 11, "x": 2, "y": 1},
                                     {"score": 6, "x": 2, "y": 2}])

        self.assertDictEqual(eval(resp.text), dict_to_check)


if __name__ == '__main__':
    unittest.main()
