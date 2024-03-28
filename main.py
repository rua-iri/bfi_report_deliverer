import logging
import re
import requests
from bs4 import BeautifulSoup
import constants
import helpers

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def find_latest_file() -> bool:
    """
    Scrape the BFI's website to find a link to the latest report
    """
    # skip download for testing only
    # TODO: remove this
    return True
    response = requests.get(url=constants.BFI_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    latestFileLink = soup.find("a", {"class": re.compile("FileDownload__Link")})

    return download_latest_file(download_url=latestFileLink.get("href"))


def download_latest_file(download_url: str) -> bool:
    """
    Download the latest copy of the BFI's weekly report
    """
    logger.info("Downloading file from: " + download_url)

    try:
        response = requests.get(url=download_url)

        with open(file=constants.FILE_DOWNLOAD_LOCATION, mode="wb") as spreadsheet_file:
            spreadsheet_file.write(response.content)

        logger.info("File downloaded successfully")
        return True

    except Exception as e:
        logger.error("Error: ", exc_info=True)
        return False


def main():
    is_download_successful = find_latest_file()

    if not is_download_successful:
        return False

    film_list = helpers.parse_spreadsheet()
    helpers.generate_html_report(film_list=film_list)

    helpers.generate_pdf_report()


if __name__ == "__main__":
    main()
