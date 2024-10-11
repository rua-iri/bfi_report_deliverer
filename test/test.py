import unittest
from os.path import exists as does_file_exist
from os import remove as delete_file

from bfi_report_deliverer.classes import Film
from bfi_report_deliverer import helpers
from bfi_report_deliverer import constants
from bfi_report_deliverer import report_deliverer


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

    def test_render_html_valid(self):
        with open("test/samples/valid_segment.html") as file:
            expected_val = file.read()

        actual_val = helpers.render_html(
            [Film(1, "asdf", "asdf", 123123, "asdf", 0.1, 123, 123, 123, 123)]
        )

        self.assertEqual(actual_val, expected_val)

    def test_render_html_empty(self):
        expected_val = "<div style='page-break-after: always;'></div>"
        actual_val = helpers.render_html([])

        self.assertEqual(actual_val, expected_val)

    def test_render_html_invalid(self):
        with self.assertRaises(AttributeError):
            helpers.render_html("test")

    def test_generate_html_report_valid(self):
        with open("test/samples/valid_report.html") as file:
            expected_val = file.read()

        sample_film = Film(1, "asdf", "asdf", 123123,
                           "asdf", 0.1, 123, 123, 123, 123)

        helpers.generate_html_report(
            [sample_film],
            [sample_film],
            [sample_film],
            "28-30 June 2024"
        )

        helpers.create_dir("reports/report.html")
        with open("reports/report.html") as file:
            actual_val = file.read()

        self.assertEqual(expected_val, actual_val)

    def test_generate_html_report_empty(self):
        with open("test/samples/empty_report.html") as file:
            expected_val = file.read()

        helpers.generate_html_report([], [], [], "28-30 June 2024")

        helpers.create_dir("reports/report.html")
        with open("reports/report.html") as file:
            actual_val = file.read()

        self.assertEqual(expected_val, actual_val)


class TestReportDeliverer(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_find_latest_file_data_valid(self):
        expected_val = (
            "https://core-cms.bfi.org.uk/media/.*/download",
            "\d+-\d+ \w+ \d{4}"
        )
        actual_val = report_deliverer.find_latest_file_data()

        self.assertRegex(actual_val[0], expected_val[0])
        self.assertRegex(actual_val[1], expected_val[1])

    def test_find_latest_file_data_invalid(self):
        expected_val = (
            "https://core-cms.bfi.org.uk/media/.*/download",
            "\d+-\d+ \w+ \d{4}"
        )
        actual_val = report_deliverer.find_latest_file_data()

        self.assertNotRegex(actual_val[1], expected_val[0])
        self.assertNotRegex(actual_val[0], expected_val[1])

    def test_download_latest_file_valid(self):
        try:
            delete_file(constants.FILE_DOWNLOAD_LOCATION)
        except FileNotFoundError:
            pass

        expected_val = "downloads/latest_report.xls"
        actual_val = report_deliverer.download_latest_file(
            "https://core-cms.bfi.org.uk/media/35623/download"
        )

        self.assertTrue(does_file_exist(constants.FILE_DOWNLOAD_LOCATION))
        self.assertTrue(expected_val in actual_val)

    def test_download_latest_file_invalid(self):
        try:
            delete_file(constants.FILE_DOWNLOAD_LOCATION)
        except FileNotFoundError:
            pass

        expected_val = "downloads/latest_report.xls"
        actual_val = report_deliverer.download_latest_file(
            "https://core-cms.bfi.org.uk/media/35623/download"
        )

        self.assertTrue(does_file_exist(constants.FILE_DOWNLOAD_LOCATION))
        self.assertTrue(expected_val in actual_val)


if __name__ == "__main__":
    unittest.main()
