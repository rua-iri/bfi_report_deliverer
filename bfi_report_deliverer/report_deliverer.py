import logging
import re
import time
import traceback
import requests
from bs4 import BeautifulSoup
from os import environ
from dotenv import load_dotenv

from bfi_report_deliverer import helpers
from bfi_report_deliverer import constants
from bfi_report_deliverer.classes import ReportsSender

LOGGING_FILE = constants.LOGGING_FILENAME.format(
    filename=time.strftime("%Y-%m-%d")
)
helpers.initialise_logs(file_name=LOGGING_FILE)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename=LOGGING_FILE,
    filemode="a",
    format=constants.LOGGING_FORMAT,
)

IS_PROD = environ.get("ENV") == "production"
load_dotenv()


def download_latest_file(download_url: str) -> str:
    """Download the latest copy of the BFI's weekly report

    Args:
        download_url (str): the link to the file

    Raises:
        e: an exception which might occur while downloading the file

    Returns:
        _type_: The original filename
    """

    try:
        logger.info("Downloading file from: " + download_url)

        response: requests.Response = requests.get(url=download_url)

        # save file using original file extension
        content_disposition: str | None = response.headers.get(
            "Content-Disposition"
        )

        if not content_disposition:
            raise Exception("Content-Disposition not found")

        file_extension_loc: int = content_disposition.find(".ods") + 1
        file_extension: str = content_disposition[file_extension_loc:]
        download_file_name: str = constants.FILE_DOWNLOAD_LOCATION.replace(
            "xlsx", file_extension
        )

        with open(file=download_file_name, mode="wb") as spreadsheet_file:
            spreadsheet_file.write(response.content)

        if file_extension != "xlsx":
            logger.info("Converting to xlsx format")
            helpers.convert_to_xlsx(download_file_name)

        logger.info("File downloaded successfully")

        return download_file_name

    except Exception as e:
        logger.error("Error Downloading File")
        logger.error("Error: ", exc_info=True)
        raise e


def find_latest_file_data() -> tuple:
    """Scrape the BFI's website to find a link to the latest report

    Raises:
        e: _description_

    Returns:
        tuple: The link to the latest version of the report and
               the weekend on which it was published
    """

    try:
        response: requests.Response = requests.get(url=constants.BFI_URL)
        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        latestFileLink = soup.find(
            "a",
            {"class": re.compile("FileDownload__Link")}
        )

        file_title = soup.find(
            "span",
            {"class": re.compile("FileDownload__Title")}
        )

        if not latestFileLink or not file_title:
            raise Exception("Unable to find file")

        return (
            latestFileLink.get("href"),
            file_title.text.split("office report: ")[1]
        )

    except Exception as e:
        logger.error("Error Finding File Location")
        logger.error("Error: ", exc_info=True)
        raise e


def main():
    try:
        logger.info("BFI Report Deliverer Start")
        logger.info("Finding Latest file")
        latest_file_url, weekend_date = find_latest_file_data()

        original_filename = download_latest_file(download_url=latest_file_url)
        logger.info("File Download Complete")

        file_hash: str = helpers.gen_file_hash(
            original_filename=original_filename
        )
        logger.info(f"File Hash: {file_hash}")

        # stop program if file matches previous version
        # if IS_PROD and not helpers.is_file_new(file_hash):
        if not helpers.is_file_new(file_hash) and IS_PROD:
            logger.error("File hash matches previous file")
            logger.info("Exiting...")
            raise Exception("File has been processed previously")
        elif IS_PROD:
            logger.info("File hash does not match previous file")

        # parse each group of films
        logger.info("Parsing: top_15")
        top_15_film_list = helpers.parse_films("top_15")

        logger.info("Parsing: other_uk")
        other_uk_film_list = helpers.parse_films("other_uk")

        logger.info("Parsing: other_new")
        other_new_film_list = helpers.parse_films(
            "other_new")

        # generate html report and convert to pdf
        helpers.generate_html_report(
            top_15_film_list=top_15_film_list,
            other_uk_film_list=other_uk_film_list,
            other_new_film_list=other_new_film_list,
            weekend_date=weekend_date,
        )
        logger.info("HTML Report Generated")

        helpers.generate_pdf_report()
        logger.info("PDF Report Generated")

        user_list = helpers.get_subscribers()
        logger.info("User List Generated")

        reportsSender = ReportsSender(user_list, weekend_date)
        reportsSender.send_reports()

        logger.info("Execution Completed")

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
