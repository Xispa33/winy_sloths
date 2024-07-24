import unittest
from api import app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_traders(self):
        response = self.app.get('/traders?min_win_rate=70')
        self.assertEqual(response.status_code, 200)

    def test_get_leaderboard(self):
        response = self.app.get('/leaderboard')
        self.assertEqual(response.status_code, 200)

    def test_stake(self):
        response = self.app.post('/stake', json={'user_id': 1, 'amount': 100})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
