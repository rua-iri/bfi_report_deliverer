from typing import Union
from constants import TMDB_IMG_URL, IMDB_URL


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

    def set_film_data(self, film_data: dict):
        if film_data.get("poster"):
            self.poster = TMDB_IMG_URL.format(filename=film_data["poster"])
        else:
            self.poster = "https://www.bfi.org.uk/dist/server/0207614d447715c2d2b9257bdd5e68b4.svg"

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
