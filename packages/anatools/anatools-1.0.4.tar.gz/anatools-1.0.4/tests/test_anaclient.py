from anatools import AnaClient
import unittest
import os

class TestSDK(unittest.TestCase):

    def setUp(self):
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('PASSWORD')
        self.env = os.getenv('ENVIRONMENT')
        self.ana = AnaClient(environment=self.env, verbose='True', email = self.email, password= self.password)
        
    def test_get_workspaces(self):
        wkspcs = self.ana.get_workspaces()
        print(wkspcs)
        assert wkspcs is not None

    def test_get_graphs(self):
        graphs = self.ana.get_graphs()
        print(graphs)
        assert graphs is not None

    def test_get_datasets(self):
        datasets = self.ana.get_datasets()
        print(datasets)
        assert datasets is not None

if __name__ == '__main__':
    unittest.main()