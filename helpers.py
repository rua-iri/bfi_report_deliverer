from hashlib import md5 as md5_hash
from time import time as unix_timestamp
import openpyxl
import openpyxl.workbook
import openpyxl.worksheet
import openpyxl.worksheet.worksheet
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
other_uk_row: list = [
    0,
]
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
        min_row=3,
        max_row=17,
        min_col=constants.MIN_COL,
        max_col=constants.MAX_COL,
        values_only=True,
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


def parse_other_uk_films():
    film_list = []
    sheet = openpyxl.load_workbook(filename=constants.FILE_DOWNLOAD_LOCATION).active

    for index, row in enumerate(
        sheet.iter_rows(
            min_row=22,
            min_col=constants.MIN_COL,
            max_col=constants.MAX_COL,
            values_only=True,
        )
    ):

        print(f"{index}: {row[RANK]}")

        if row[0] == None:
            other_uk_row.append(index + other_uk_row[0])
            break

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

    print(film_list)

    print(other_uk_row)


def parse_other_new_releases():
    film_list = []
    sheet = openpyxl.load_workbook(filename=constants.FILE_DOWNLOAD_LOCATION).active

    for row in sheet.iter_rows(
        min_row=other_uk_row[1],
        min_col=constants.MIN_COL,
        max_col=constants.MAX_COL,
        values_only=True,
    ):

        # print(row)

        if row[0] == None:
            break

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

    print(film_list)


def generate_html_report(film_list) -> None:
    """
    Generate the new html report using the html templates
    """
    base_html = jinja_environment.get_template(constants.BASE_HTML_TEMPLATE)
    table_row_html = jinja_environment.get_template(constants.TABLE_ROW_TEMPLATE)

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


def gen_file_hash() -> str:
    """Generate a hash of the excel report file downloaded

    Returns:
        str: An md5 hash of the file
    """

    h_lib = md5_hash()

    with open(constants.FILE_DOWNLOAD_LOCATION, "rb") as file:
        chunk = 0
        while chunk != b"":
            chunk = file.read(1024)
            h_lib.update(chunk)

    return h_lib.hexdigest()


def is_file_new(file_hash: str) -> bool:
    """Check whether the file downloaded has been processed before and insert
    the new file's hash into the database

    Args:
        file_hash (str): An md5 hash of the file from gen_file_hash()

    Returns:
        bool: Whether the file is new or not
    """

    cursor = con.cursor()
    result = cursor.execute(constants.SELECT_FILES_QUERY, (file_hash,)).fetchall()
    print(result)
    print(not result)

    timestamp = int(unix_timestamp())

    cursor.execute(constants.INSERT_FILE_QUERY, (file_hash, timestamp))
    con.commit()

    if len(result) == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    is_file_new("67089608790baa07d928c8d5f51b5c28")
