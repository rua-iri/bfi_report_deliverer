import logging
import re
import requests
import resend
from bs4 import BeautifulSoup
import constants
import helpers


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

WEEKEND_DATES = [0, 0]


def find_latest_file() -> bool:
    """
    Scrape the BFI's website to find a link to the latest report
    """
    # skip download for development only (we don't need to download the newest version every time)
    # TODO: remove this
    return True
    response = requests.get(url=constants.BFI_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    latestFileLink = soup.find("a", {"class": re.compile("FileDownload__Link")})


    # TODO: get the week's dates from the filename here
    file_title = soup.find("span", {"class": re.compile("FileDownload__Title")})
    WEEKEND_DATES = file_title.text.split('office report: ')[1].split(' ')[0].split('-')
    

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

def send_report(user_name, email_address):
    resend.api_key = "apikey_goes_here"

    # TODO: format email content using the user's details

    email_subject = ""
    
    with open(constants.HTML_EMAIL_LOCATION, "r") as html_file:
        html_content = html_file.read()
        html_content.format(user_name=user_name, week_number=0)

    parameters = {
        "From": "fromemail",
        "to": [email_address],
        "subject": email_subject,
        "html": html_content,
    }

    email = resend.Emails.send(params=parameters)
    logger.info(email)

    

def main():
    is_download_successful = find_latest_file()

    if not is_download_successful:
        return False

    film_list = helpers.parse_spreadsheet()
    helpers.generate_html_report(film_list=film_list)

    helpers.generate_pdf_report()

    user_list = helpers.get_subscribers()



if __name__ == "__main__":
    main()
