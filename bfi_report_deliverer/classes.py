from typing import Union
from os import environ
import json
import jinja2
import resend
import logging
import requests

from . import helpers
from .constants import (
    TMDB_IMG_URL,
    IMDB_URL,
    TMDB_SEARCH_API_URL,
    TMDB_DETAILS_API_URL,
    PDF_REPORT_LOCATION
)


class Film:
    def __init__(
        self,
        rank: int,
        title: str,
        origin_country: str,
        weekend_gross: int,
        distributor: str,
        weekly_change: Union[float, str],
        weeks_on_release: int,
        cinema_number: int,
        site_average: int,
        total_gross: int,
    ):
        self.rank: int = rank
        self.title: str = title
        self.origin_country: str = origin_country
        self.weekend_gross: str = "{:,}".format(weekend_gross)
        self.distributor: str = distributor
        self.set_weekly_change(weekly_change)
        self.weeks_on_release: int = weeks_on_release
        self.cinema_number: int = cinema_number
        self.site_average: str = "{:,}".format(site_average)
        self.total_gross: str = "{:,}".format(total_gross)

    def set_weekly_change(self, weekly_change: Union[float, str]):
        if type(weekly_change) is float:
            self.weekly_change = round(weekly_change, 2)
        else:
            self.weekly_change = weekly_change

    def fetch_film_data(self):
        """Fetch film data from TMDB api

        Args:
            film (Film): an instance of the Film class

        Returns:
            dict: a dictionary containing detailed information about the film
        """

        response = requests.get(
            TMDB_SEARCH_API_URL.format(query=self.title.split("(")[0]),
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {environ.get("TMBD_API_KEY")}",
            },
        )

        film_data = json.loads(response.text)

        if film_data["total_results"] == 0:
            return {}

        film_id = film_data["results"][0]["id"]

        response = requests.get(
            TMDB_DETAILS_API_URL.format(id=film_id),
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {environ.get("TMBD_API_KEY")}",
            },
        )

        film_data = json.loads(response.text)

        return {
            "poster": film_data["poster_path"],
            "imdb_id": film_data["imdb_id"]
        }

    def set_film_data(self):
        film_data = self.fetch_film_data()

        if film_data.get("poster"):
            self.poster = TMDB_IMG_URL.format(filename=film_data["poster"])
        else:
            self.poster = "https://rua-iri.com/images/bfi/bfi_logo.png"

        if film_data.get("imdb_id"):
            self.imdb = IMDB_URL.format(id=film_data["imdb_id"])
        else:
            self.imdb = "https://www.imdb.com/"

    def __repr__(self):
        return (
            f"Rank: {self.rank},"
            + f" Title:{self.title},"
            + f" Country of Origin: {self.origin_country},"
            + f" Weekend Gross: {self.weekend_gross}, "
            + f" Distributor: {self.distributor}, "
            + f" Weekly Change: {self.weekly_change}, "
            + f" Weeks on Release: {self.weeks_on_release}, "
            + f" Number of cinemas: {self.cinema_number}, "
            + f" Site Average: {self.site_average}, "
            + f" Total Gross: {self.total_gross}"
        )


class ReportsSender:
    def __init__(self, user_list: list, weekend_date: str) -> None:
        self.user_list = user_list
        self.weekend_date = weekend_date
        self.is_prod = environ.get("ENV") == "production"
        self.logger = logging.getLogger(__name__)
        self.jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates")
        )

    def send_reports(self):
        if self.is_prod:
            for user in self.user_list:
                self.send_report_to_user(
                    user_name=user["first_name"],
                    email_address=user["email"],
                )

                self.logger.info(
                    f"Report Sent to {user['first_name']} {user['last_name']}"
                )

            self.logger.info("Reports Sent")

    def send_report_to_user(self, user_name: str, email_address: str):
        """Send email to subscriber with report file attached

        Args:
            user_name (str): the name of the user
            email_address (str): the email address of the user

        Raises:
            e: exception which might occur while sending the email
        """
        try:
            resend.api_key = environ.get("RESEND_API_KEY")

            email_subject = f"BFI Report: {self.weekend_date}"

            html_content = self.generate_email_body(
                user_name=user_name,
                week_number=self.weekend_date
            )

            helpers.create_dir(PDF_REPORT_LOCATION)
            with open(PDF_REPORT_LOCATION, "rb") as report_file:
                attachment = list(report_file.read())

            report_filename = self.weekend_date.replace(" ", "_")

            parameters: resend.Emails.SendParams = {
                "from": environ.get("FROM_EMAIL", ""),
                "to": [email_address],
                "subject": email_subject,
                "html": html_content,
                "attachments": [
                    {
                        "filename": f"{report_filename}_report.pdf",
                        "content": attachment
                    }
                ],
            }

            email = resend.Emails.send(params=parameters)
            self.logger.info(email)

        except Exception as e:
            self.logger.error("Error in sending report")
            raise e

    def generate_email_body(self, user_name: str, week_number: str) -> str:
        """Generate the body of the email to be sent to subscribers

        Args:
            user_name (str): The user to whom the email will be sent
            week_number (str): The date of the previous weekend

        Returns:
            str: html content of the email
        """

        email_template = self.jinja_environment.get_template("email.html")
        return email_template.render(
            user_name=user_name,
            week_number=week_number
        )
