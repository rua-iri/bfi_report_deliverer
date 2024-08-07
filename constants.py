LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] - %(message)s"
LOGGING_FILENAME = "logs/{filename}.log"
LOGGING_SEPARATOR = "-------------------------\n"

BFI_URL = "https://www.bfi.org.uk/industry-data-insights/weekend-box-office-figures"

FILE_DOWNLOAD_LOCATION = "downloads/latest_report.xlsx"


MIN_COL = 1
MAX_COL = 10

TOP_15_MIN = 3
TOP_15_MAX = 17


BASE_HTML_TEMPLATE = "_base.html"
CARD_TEMPLATE = "card.html"
HTML_REPORT_LOCATION = "reports/report.html"
PDF_REPORT_LOCATION = "reports/report.pdf"

HTML_PAGE_BREAK = "<div style='page-break-after: always;'></div>"

TMDB_SEARCH_API_URL = "https://api.themoviedb.org/3/search/movie?query={query}"
TMDB_DETAILS_API_URL = "https://api.themoviedb.org/3/movie/{id}"

TMDB_IMG_URL = "https://image.tmdb.org/t/p/w200{filename}"
IMDB_URL = "https://www.imdb.com/title/{id}"
