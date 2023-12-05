import logging
import requests
from bs4 import BeautifulSoup
import constants

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def main():
    is_download_successful = find_latest_file()

    if is_download_successful:
        pass


def find_latest_file() -> bool:
    response = requests.get(url=constants.BFI_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    latestFileLink = soup.find("a", {"class": "FileDownload__Link-sc-ix3u4x-1"})

    return download_latest_file(download_url=latestFileLink.get("href"))


def download_latest_file(download_url: str) -> bool:
    print(download_url)

    try:
        response = requests.get(url=download_url)

        with open(file=constants.FILE_DOWNLOAD_LOCATION, mode="wb") as spreadsheet_file:
            spreadsheet_file.write(response.content)

        return True

    except Exception as e:
        logger.error("Error: ", exc_info=True)
        return False


if __name__ == "__main__":
    main()
