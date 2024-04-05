import openpyxl
import constants
import pdfkit
import sqlite3
import jinja2
from classes import Film
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


top_15_row: list = [3, 17]
other_uk_row: list = [0, 0]
other_new_row: list = [0, 0]

con = sqlite3.connect("bfi_report.db")
con.row_factory = sqlite3.Row

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))


def find_section(start_row, section_name):
    """
    Locate the sections in the spreadsheet for other uk films and new releases
    """

    sheet = openpyxl.load_workbook(
        filename=constants.FILE_DOWNLOAD_LOCATION, read_only=True, data_only=True
    ).active

    for index, row in enumerate(
        sheet.iter_rows(min_row=start_row, min_col=2, max_col=2, values_only=True)
    ):

        if section_name == "other uk films":
            if str(row[0]).lower() == section_name:
                other_uk_row[0] = index + 1 + start_row

            elif other_uk_row[0] != 0 and not row[0]:
                other_uk_row[1] = index - 1 + start_row
                break

        if section_name == "other new releases":
            if str(row[0]).lower() == section_name:
                other_new_row[0] = index + 1 + start_row

            elif other_new_row[0] != 0 and not row[0]:
                other_new_row[1] = index - 1 + start_row
                break


def parse_spreadsheet() -> list:
    """
    Parse the spreadsheet and a return a list of the top 15 films
    """
    film_list = []

    sheet = openpyxl.load_workbook(
        filename=constants.FILE_DOWNLOAD_LOCATION, read_only=True, data_only=True
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


def generate_html_report(film_list) -> None:
    """
    Generate the new html report using the html templates
    """
    base_html = jinja_environment.get_template("_base.html")
    table_row_html = jinja_environment.get_template("table_row.html")

    complete_table_html = ""

    # generate table rows and append them to complete table string
    for film in film_list:
        table_row = table_row_html.render(film.__dict__)
        # table_row = table_row_html.format(film)
        complete_table_html += table_row

    # write content to html
    with open(constants.HTML_REPORT_LOCATION, "w") as file:
        file.write(base_html.render(top_15_contents=complete_table_html))


def generate_pdf_report() -> None:
    """
    Generate the new pdf report using the html template
    """
    pdfkit.from_file(
        input=constants.HTML_REPORT_LOCATION, output_path=constants.PDF_REPORT_LOCATION
    )


def get_subscribers():
    """
    Query database for list of all currently active subscribers
    """
    cursor = con.cursor()
    res = cursor.execute(
        constants.SELECT_USERS_QUERY,
    )
    user_list = res.fetchall()

    return user_list


def generate_email_body(user_name: str, week_number: str) -> str:
    """
    Generate the body of the email to be sent to subscribers
    """

    email_template = jinja_environment.get_template("email.html")
    return email_template.render(user_name=user_name, week_number=week_number)


def create_db():
    """
    Create users table in database (should only run on initialising repository)
    """
    cursor = con.cursor()

    res = cursor.execute(constants.CREATE_TABLE_QUERY)

    res.fetchall()
