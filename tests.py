import unittest
import os
import dota2

class DotaTest(unittest.TestCase):

    def get_api(self):
        return dota2.Dota2(os.environ['DOTA_API_KEY'])

    def get_match_history(self):
        d = self.get_api()
        h = d.find_match_history()
        return h

    def test_key_is_valid(self):
        d = self.get_api()
        self.assertTrue(d.is_valid)

    def test_find_match_history(self):
        h = self.get_match_history()
        self.assertTrue(len(h) > 10)

    def test_find_match_id(self):
        h = self.get_match_history()
        self.assertTrue(h[0].id != None)

    def test_find_players(self):
        h = self.get_match_history()
        for m in h:
            self.assertTrue(len(m.players) > 0)

if __name__ == '__main__':
    unittest.main()
