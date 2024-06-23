import logging
import re
import requests
import resend
from bs4 import BeautifulSoup
import constants
import helpers
import os
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

WEEKEND_DATE = ""
load_dotenv()


def find_latest_file() -> None:
    """
    Scrape the BFI's website to find a link to the latest report
    """
    global WEEKEND_DATE
    # skip download for development only (we don't need to download the newest version every time)
    # TODO: remove this
    # return True
    response = requests.get(url=constants.BFI_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    latestFileLink = soup.find("a", {"class": re.compile("FileDownload__Link")})

    file_title = soup.find("span", {"class": re.compile("FileDownload__Title")})
    WEEKEND_DATE = file_title.text.split("office report: ")[1]

    download_latest_file(download_url=latestFileLink.get("href"))


def download_latest_file(download_url: str) -> None:
    """
    Download the latest copy of the BFI's weekly report
    """
    logger.info("Downloading file from: " + download_url)

    try:
        response = requests.get(url=download_url)

        with open(file=constants.FILE_DOWNLOAD_LOCATION, mode="wb") as spreadsheet_file:
            spreadsheet_file.write(response.content)

        logger.info("File downloaded successfully")

    except Exception as e:
        logger.error("Error Downloading File")
        logger.error("Error: ", exc_info=True)
        raise e


def send_report(user_name: str, email_address: str):
    """
    Send email to subscriber with report file attached
    """
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")

        email_subject = f"BFI Report: {WEEKEND_DATE}"

        html_content = helpers.generate_email_body(
            user_name=user_name, week_number=WEEKEND_DATE
        )

        with open(constants.PDF_REPORT_LOCATION, "rb") as report_file:
            attachment = list(report_file.read())

        report_filename = WEEKEND_DATE.replace(" ", "_")

        parameters = {
            "from": os.getenv("FROM_EMAIL"),
            "to": [email_address],
            "subject": email_subject,
            "html": html_content,
            "attachments": [
                {"filename": f"{report_filename}_report.pdf", "content": attachment}
            ],
        }

        email = resend.Emails.send(params=parameters)
        logger.info(email)

    except Exception as e:
        logger.error("Error in sending report")
        raise e


def main():

    try:
        # find_latest_file()
        # logger.info("Download Complete")
        # file_hash: str = helpers.gen_file_hash()

        # if helpers.is_file_new(file_hash):
        #     # TODO: implement some way to handle this error and delay the program's execution for another day
        #     pass

        top_15_film_list = helpers.parse_films("top_15")
        other_uk_film_list = helpers.parse_films("other_uk")
        other_new_film_list = helpers.parse_films("other_new")
        helpers.generate_html_report(
            top_15_film_list=top_15_film_list,
            other_uk_film_list=other_uk_film_list,
            other_new_film_list=other_new_film_list,
            weekend_date=WEEKEND_DATE,
        )
        helpers.generate_pdf_report()
        logger.info("Report Generated")

        # user_list = helpers.get_subscribers()
        # logger.info("User List Generated")

        # TODO: uncomment this later
        # for user in user_list:
        #     send_report(user_name=user["first_name"], email_address=user["email"])
        #     logger.info(f"Report Sent to {user['first_name']} {user['last_name']}")

        logger.info("Reports Sent")

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
