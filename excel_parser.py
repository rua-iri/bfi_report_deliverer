import openpyxl
from classes import Film
from constants import FILE_DOWNLOAD_LOCATION
from mapping import (
    RANK,
    TITLE,
    ORIGIN_COUNTRY,
    WEEKEND_GROSS,
    DISTRIBUTOR,
    WEEKLY_CHANGE,
    WEEKS_ON_RELEASE,
    CINEMA_NUMBER,
    SITE_AVERAGE,
    TOTAL_GROSS,
)


def parse_spreadsheet():
    film_list = []

    sheet = openpyxl.load_workbook(
        filename=FILE_DOWNLOAD_LOCATION, read_only=True, data_only=True
    ).active

    # iterate through first 15 films
    for row in sheet.iter_rows(
        min_row=3, max_row=17, min_col=1, max_col=10, values_only=True
    ):

        film = Film(
            rank=row[RANK],
            title=row[TITLE],
            origin_country=row[ORIGIN_COUNTRY],
            weekend_gross=row[WEEKEND_GROSS],
            distributor=row[DISTRIBUTOR],
            weekly_change=row[WEEKLY_CHANGE],
            weeks_on_release=row[WEEKS_ON_RELEASE],
            cinema_number=row[CINEMA_NUMBER],
            site_average=row[SITE_AVERAGE],
            total_gross=row[TOTAL_GROSS],
        )

        film_list.append(film)

    
    return film_list
