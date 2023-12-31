import openpyxl
import constants
import pdfkit
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


def parse_spreadsheet() -> list:
    """
    Parse the spreadsheet and a return a list of the top 15 films
    """
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


def get_template_strings() -> tuple:
    """
    Load the html templates as strings to be formatted later
    """

    with open(constants.BASE_HTML_TEMPLATE) as file:
        base_html = file.read()

    with open(constants.TABLE_ROW_TEMPLATE) as file:
        table_row_html = file.read()

    return (base_html, table_row_html)


def generate_html_report(film_list) -> None:
    """
    Generate the new html report using the html templates
    """
    base_html, table_row_html = get_template_strings()
    complete_table_html = ""

    # generate table rows and append them to complete table string
    for film in film_list:
        table_row = table_row_html.format(film)
        complete_table_html += table_row

    # write content to html
    with open(constants.HTML_REPORT_LOCATION, "w") as file:
        file.write(base_html.format(top_15_contents=complete_table_html))



def generate_pdf_report() -> None:
    """
    Generate the new pdf report using the html template
    """

    # pdfkit.from_file(input=constants.HTML_REPORT_LOCATION, output_path=constants.PDF_REPORT_LOCATION)
    # pdfkit.from_string(input=film_page_html, output_path=constants.PDF_REPORT_LOCATION)
