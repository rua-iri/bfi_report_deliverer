import unittest
from classes import Film
import helpers


class TestHelpers(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_fetch_film_data_valid(self):
        expected_val = {
            'poster': '/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg',
            'imdb_id': 'tt22022452'
        }

        film = Film(
            rank=1,
            title="Inside Out 2",
            origin_country="USA",
            weekend_gross=6003527,
            distributor="Disney",
            weekly_change=23,
            weeks_on_release=3,
            cinema_number=719,
            site_average=8350,
            total_gross=31963087
        )
        actual_val = helpers.fetch_film_data(film)
        self.assertEqual(actual_val, expected_val)
        self.assertNotEqual(actual_val, {})

    def test_fetch_film_data_invalid(self):
        expected_val = {
            'poster': '/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg',
            'imdb_id': 'tt22022452'
        }

        film = Film(
            rank=1,
            title="Inside Oot 2",
            origin_country="USA",
            weekend_gross=6003527,
            distributor="Disney",
            weekly_change=23,
            weeks_on_release=3,
            cinema_number=719,
            site_average=8350,
            total_gross=31963087
        )
        actual_val = helpers.fetch_film_data(film)

        self.assertEqual(actual_val, {})
        self.assertNotEqual(actual_val, expected_val)

    def test_parse_films_valid(self):
        actual_val = helpers.parse_films("top_15", "downloads/example.xlsx")

        for film in actual_val:
            self.assertEqual(type(film), Film)

        self.assertEqual(len(actual_val), 15)

    def test_parse_films_invalid(self):
        with self.assertRaises(Exception):
            helpers.parse_films("top_15asdf", "downloads/example.xlsx")


if __name__ == "__main__":
    unittest.main()
