import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

URL = "https://www.bfi.org.uk/industry-data-insights/weekend-box-office-figures"


def main():
    is_download_successful = find_latest_file()

    if is_download_successful:
        pass


def find_latest_file():
    response = requests.get(url=URL)
    soup = BeautifulSoup(response.text, "html.parser")
    latestFileLink = soup.find("a", {"class": "FileDownload__Link-sc-ix3u4x-1"})

    return download_latest_file(download_url=latestFileLink.get("href"))


def download_latest_file(download_url: str):
    print(download_url)

    try:
        response = requests.get(url=download_url)

        with open(file="downloads/latest_report.xlsx", mode="wb") as spreadsheet_file:
            spreadsheet_file.write(response.content)

        return True

    except Exception as e:
        logger.error("Error: ", exc_info=True)
        return False


if __name__ == "__main__":
    main()
