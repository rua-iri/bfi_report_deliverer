class Film:
    def __init__(
        self,
        rank,
        title,
        origin_country,
        weekend_gross,
        distributor,
        weekly_change,
        weeks_on_release,
        cinema_number,
        site_average,
        total_gross,
    ):
        self.rank = rank
        self.title = title
        self.origin_country = origin_country
        self.weekend_gross = weekend_gross
        self.distributor = distributor
        self.weekly_change = weekly_change
        self.weeks_on_release = weeks_on_release
        self.cinema_number = cinema_number
        self.site_average = site_average
        self.total_gross = total_gross

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
