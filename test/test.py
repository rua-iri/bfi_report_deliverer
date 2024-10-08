import unittest
from os.path import exists as does_file_exist
from os import remove as delete_file

from bfi_report_deliverer.classes import Film
from bfi_report_deliverer import helpers
from bfi_report_deliverer import constants
from bfi_report_deliverer import main


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
        expected_val = """<div class="card my-3">
    <div class="row g-0">
        <div class="col-4 d-flex">
            <img class="img-fluid rounded-start bg-dark" alt="film poster" src="">
        </div>
        <div class="col-8">
            <div class="card-body">
                <h4 class="card-title d-flex justify-content-between">
                    <div>
                        asdf
                    </div>
                    <div class="fw-bold">
                        #1
                    </div>
                </h4>


                <div class="my-2">
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Country of Origin:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weekend Gross:
                        </span>
                        £123,123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Distributor:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Change on Last Week:
                        </span>
                        0.1%
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weeks on Release:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Number of Cinemas:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Site Average:
                        </span>
                        £123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Total Gross to Date:
                        </span>
                        £123
                    </p>
                </div>

                <a class="btn btn-lg btn-info" href="" target="_blank">
                    IMDB
                </a>

            </div>
        </div>
    </div>
</div><div style='page-break-after: always;'></div>"""
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
        expected_val = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BFI Weekly Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <style>
        body {
            font-family: sans-serif;
        }
    </style>
</head>

<body>
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <?xml version="1.0" encoding="UTF-8"?>
            <svg width="98px" height="100px" viewBox="0 0 98 100" version="1.1" xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink">
                <!-- Generator: Sketch 61.2 (89653) - https://sketch.com -->
                <title>Branding / BFI Logo / Black</title>
                <desc>Created with Sketch.</desc>
                <g id="Branding-/-BFI-Logo-/-Black" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <g id="BFI-Logo-Copy" fill="#1c1c1c">
                        <path
                            d="M28.0268,15.3963 C28.0268,13.4183 27.2448,12.3063 26.0908,11.6473 C25.2678,11.1943 24.4018,11.1103 22.8368,11.1103 L19.8298,11.1103 L19.7468,20.0093 L22.8778,20.0093 C26.0078,20.0093 28.0268,18.3613 28.0268,15.3963"
                            id="Fill-15"></path>
                        <path
                            d="M23.7001,23.6355 L19.7461,23.6355 L19.6641,33.1925 L23.4561,33.1925 C26.7901,33.1925 29.5111,31.7905 29.5111,28.3305 C29.5111,25.1185 26.7081,23.6355 23.7001,23.6355"
                            id="Fill-16"></path>
                        <path
                            d="M80.422,66.402 C80.315,66.402 80.211,66.416 80.104,66.418 C81.703,62.801 82.607,58.808 82.607,54.599 C82.607,38.419 69.493,25.303 53.313,25.303 C50.451,25.303 47.692,25.733 45.077,26.498 C45.285,25.263 45.418,24.002 45.418,22.708 C45.418,10.166 35.25,0 22.71,0 C10.166,0 0,10.166 0,22.708 C0,35.248 10.166,45.416 22.71,45.416 C23.686,45.416 24.641,45.334 25.584,45.215 C24.586,48.164 24.021,51.312 24.021,54.599 C24.021,70.775 37.136,83.89 53.313,83.89 C56.984,83.89 60.481,83.185 63.719,81.953 C63.69,82.356 63.658,82.758 63.658,83.168 C63.658,92.427 71.163,99.933 80.422,99.933 C89.682,99.933 97.187,92.427 97.187,83.168 C97.187,73.908 89.682,66.402 80.422,66.402 L80.422,66.402 Z M24.194,36.57 L12.124,36.57 L12.124,33.192 L15.01,33.192 L15.174,11.111 L12.124,11.111 L12.124,7.731 L23.618,7.731 C26.627,7.731 28.522,8.063 30.294,9.379 C31.652,10.37 32.889,12.388 32.889,14.817 C32.889,18.157 30.827,21.122 27.163,21.41 L27.163,21.491 C31.035,21.45 34.617,24.088 34.617,28.496 C34.617,33.397 31.157,36.57 24.194,36.57 L24.194,36.57 Z M63.673,52.535 L63.673,57.423 L51.562,57.423 L51.452,70.31 L56.227,70.31 L56.227,74.865 L41.287,74.865 L41.287,70.31 L45.175,70.31 L45.397,40.536 L40.897,40.536 L40.897,36.263 L40.897,35.98 L41.108,35.98 L68.227,35.98 L68.45,46.2 L63.283,46.2 L62.95,40.536 L51.674,40.536 L51.562,52.535 L63.673,52.535 Z M84.526,75.592 L82.606,75.592 L82.606,90.709 L84.526,90.709 L84.526,93.818 L76.236,93.818 L76.236,90.709 L78.157,90.709 L78.157,75.592 L76.236,75.592 L76.236,72.805 L76.236,72.485 L76.476,72.485 L84.526,72.485 L84.526,75.592 Z"
                            id="Fill-17"></path>
                    </g>
                </g>
            </svg>
            <span class="navbar-brand mb-0 h1">Weekly Report: 28-30 June 2024</span>
        </div>
    </nav>
    <div class="container">

        <div class="my-5">
            <h2 class="my-5">This Week's Top 15</h2>
            <div class="card my-3">
    <div class="row g-0">
        <div class="col-4 d-flex">
            <img class="img-fluid rounded-start bg-dark" alt="film poster" src="">
        </div>
        <div class="col-8">
            <div class="card-body">
                <h4 class="card-title d-flex justify-content-between">
                    <div>
                        asdf
                    </div>
                    <div class="fw-bold">
                        #1
                    </div>
                </h4>


                <div class="my-2">
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Country of Origin:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weekend Gross:
                        </span>
                        £123,123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Distributor:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Change on Last Week:
                        </span>
                        0.1%
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weeks on Release:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Number of Cinemas:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Site Average:
                        </span>
                        £123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Total Gross to Date:
                        </span>
                        £123
                    </p>
                </div>

                <a class="btn btn-lg btn-info" href="" target="_blank">
                    IMDB
                </a>

            </div>
        </div>
    </div>
</div><div style='page-break-after: always;'></div>
        </div>
        <div class="my-5">
            <h2 class="my-5">Other UK films</h2>
            <div class="card my-3">
    <div class="row g-0">
        <div class="col-4 d-flex">
            <img class="img-fluid rounded-start bg-dark" alt="film poster" src="">
        </div>
        <div class="col-8">
            <div class="card-body">
                <h4 class="card-title d-flex justify-content-between">
                    <div>
                        asdf
                    </div>
                    <div class="fw-bold">
                        #1
                    </div>
                </h4>


                <div class="my-2">
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Country of Origin:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weekend Gross:
                        </span>
                        £123,123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Distributor:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Change on Last Week:
                        </span>
                        0.1%
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weeks on Release:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Number of Cinemas:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Site Average:
                        </span>
                        £123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Total Gross to Date:
                        </span>
                        £123
                    </p>
                </div>

                <a class="btn btn-lg btn-info" href="" target="_blank">
                    IMDB
                </a>

            </div>
        </div>
    </div>
</div><div style='page-break-after: always;'></div>
        </div>
        <div class="my-5">
            <h2 class="my-5">Other new releases</h2>
            <div class="card my-3">
    <div class="row g-0">
        <div class="col-4 d-flex">
            <img class="img-fluid rounded-start bg-dark" alt="film poster" src="">
        </div>
        <div class="col-8">
            <div class="card-body">
                <h4 class="card-title d-flex justify-content-between">
                    <div>
                        asdf
                    </div>
                    <div class="fw-bold">
                        #1
                    </div>
                </h4>


                <div class="my-2">
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Country of Origin:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weekend Gross:
                        </span>
                        £123,123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Distributor:
                        </span>
                        asdf
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Change on Last Week:
                        </span>
                        0.1%
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Weeks on Release:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Number of Cinemas:
                        </span>
                        123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Site Average:
                        </span>
                        £123
                    </p>
                    <p class="card-text my-0">
                        <span class="fw-bold">
                            Total Gross to Date:
                        </span>
                        £123
                    </p>
                </div>

                <a class="btn btn-lg btn-info" href="" target="_blank">
                    IMDB
                </a>

            </div>
        </div>
    </div>
</div><div style='page-break-after: always;'></div>
        </div>
        

    </div>
</body>

</html>"""

        sample_film = Film(1, "asdf", "asdf", 123123,
                           "asdf", 0.1, 123, 123, 123, 123)

        helpers.generate_html_report(
            [sample_film],
            [sample_film],
            [sample_film],
            "28-30 June 2024"
        )

        with open("reports/report.html") as file:
            actual_val = file.read()

        self.assertEqual(expected_val, actual_val)

    def test_generate_html_report_empty(self):
        expected_val = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BFI Weekly Report</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <style>
        body {
            font-family: sans-serif;
        }
    </style>
</head>

<body>
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <?xml version="1.0" encoding="UTF-8"?>
            <svg width="98px" height="100px" viewBox="0 0 98 100" version="1.1" xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink">
                <!-- Generator: Sketch 61.2 (89653) - https://sketch.com -->
                <title>Branding / BFI Logo / Black</title>
                <desc>Created with Sketch.</desc>
                <g id="Branding-/-BFI-Logo-/-Black" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                    <g id="BFI-Logo-Copy" fill="#1c1c1c">
                        <path
                            d="M28.0268,15.3963 C28.0268,13.4183 27.2448,12.3063 26.0908,11.6473 C25.2678,11.1943 24.4018,11.1103 22.8368,11.1103 L19.8298,11.1103 L19.7468,20.0093 L22.8778,20.0093 C26.0078,20.0093 28.0268,18.3613 28.0268,15.3963"
                            id="Fill-15"></path>
                        <path
                            d="M23.7001,23.6355 L19.7461,23.6355 L19.6641,33.1925 L23.4561,33.1925 C26.7901,33.1925 29.5111,31.7905 29.5111,28.3305 C29.5111,25.1185 26.7081,23.6355 23.7001,23.6355"
                            id="Fill-16"></path>
                        <path
                            d="M80.422,66.402 C80.315,66.402 80.211,66.416 80.104,66.418 C81.703,62.801 82.607,58.808 82.607,54.599 C82.607,38.419 69.493,25.303 53.313,25.303 C50.451,25.303 47.692,25.733 45.077,26.498 C45.285,25.263 45.418,24.002 45.418,22.708 C45.418,10.166 35.25,0 22.71,0 C10.166,0 0,10.166 0,22.708 C0,35.248 10.166,45.416 22.71,45.416 C23.686,45.416 24.641,45.334 25.584,45.215 C24.586,48.164 24.021,51.312 24.021,54.599 C24.021,70.775 37.136,83.89 53.313,83.89 C56.984,83.89 60.481,83.185 63.719,81.953 C63.69,82.356 63.658,82.758 63.658,83.168 C63.658,92.427 71.163,99.933 80.422,99.933 C89.682,99.933 97.187,92.427 97.187,83.168 C97.187,73.908 89.682,66.402 80.422,66.402 L80.422,66.402 Z M24.194,36.57 L12.124,36.57 L12.124,33.192 L15.01,33.192 L15.174,11.111 L12.124,11.111 L12.124,7.731 L23.618,7.731 C26.627,7.731 28.522,8.063 30.294,9.379 C31.652,10.37 32.889,12.388 32.889,14.817 C32.889,18.157 30.827,21.122 27.163,21.41 L27.163,21.491 C31.035,21.45 34.617,24.088 34.617,28.496 C34.617,33.397 31.157,36.57 24.194,36.57 L24.194,36.57 Z M63.673,52.535 L63.673,57.423 L51.562,57.423 L51.452,70.31 L56.227,70.31 L56.227,74.865 L41.287,74.865 L41.287,70.31 L45.175,70.31 L45.397,40.536 L40.897,40.536 L40.897,36.263 L40.897,35.98 L41.108,35.98 L68.227,35.98 L68.45,46.2 L63.283,46.2 L62.95,40.536 L51.674,40.536 L51.562,52.535 L63.673,52.535 Z M84.526,75.592 L82.606,75.592 L82.606,90.709 L84.526,90.709 L84.526,93.818 L76.236,93.818 L76.236,90.709 L78.157,90.709 L78.157,75.592 L76.236,75.592 L76.236,72.805 L76.236,72.485 L76.476,72.485 L84.526,72.485 L84.526,75.592 Z"
                            id="Fill-17"></path>
                    </g>
                </g>
            </svg>
            <span class="navbar-brand mb-0 h1">Weekly Report: 28-30 June 2024</span>
        </div>
    </nav>
    <div class="container">

        <div class="my-5">
            <h2 class="my-5">This Week's Top 15</h2>
            <div style='page-break-after: always;'></div>
        </div>
        <div class="my-5">
            <h2 class="my-5">Other UK films</h2>
            <div style='page-break-after: always;'></div>
        </div>
        <div class="my-5">
            <h2 class="my-5">Other new releases</h2>
            <div style='page-break-after: always;'></div>
        </div>
        

    </div>
</body>

</html>"""

        helpers.generate_html_report([], [], [], "28-30 June 2024")

        with open("reports/report.html") as file:
            actual_val = file.read()

        self.assertEqual(expected_val, actual_val)


class TestMain(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_find_latest_file_data_valid(self):
        expected_val = (
            "https://core-cms.bfi.org.uk/media/.*/download",
            "\d+-\d+ \w+ \d{4}"
        )
        actual_val = main.find_latest_file_data()

        self.assertRegex(actual_val[0], expected_val[0])
        self.assertRegex(actual_val[1], expected_val[1])

    def test_find_latest_file_data_invalid(self):
        expected_val = (
            "https://core-cms.bfi.org.uk/media/.*/download",
            "\d+-\d+ \w+ \d{4}"
        )
        actual_val = main.find_latest_file_data()

        self.assertNotRegex(actual_val[1], expected_val[0])
        self.assertNotRegex(actual_val[0], expected_val[1])

    def test_download_latest_file_valid(self):
        try:
            delete_file(constants.FILE_DOWNLOAD_LOCATION)
        except FileNotFoundError:
            pass

        expected_val = "downloads/latest_report.xls"
        actual_val = main.download_latest_file(
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
        actual_val = main.download_latest_file(
            "https://core-cms.bfi.org.uk/media/35623/download"
        )

        self.assertTrue(does_file_exist(constants.FILE_DOWNLOAD_LOCATION))
        self.assertTrue(expected_val in actual_val)


if __name__ == "__main__":
    unittest.main()
