BFI_URL = "https://www.bfi.org.uk/industry-data-insights/weekend-box-office-figures"

FILE_DOWNLOAD_LOCATION = "downloads/latest_report.xlsx"


MIN_COL=1
MAX_COL=10


BASE_HTML_TEMPLATE = "_base.html"
TABLE_ROW_TEMPLATE = "table_row.html"
HTML_REPORT_LOCATION = "reports/report.html"
PDF_REPORT_LOCATION = "reports/report.pdf"
HTML_EMAIL_LOCATION = "email.html"

SELECT_USERS_QUERY = "SELECT * FROM users WHERE is_active = TRUE;"
CREATE_TABLE_QUERY = """
CREATE TABLE users
(
id INTEGER PRIMARY KEY,
first_name TEXT,
last_name TEXT,
email TEXT,
is_active BOOL
)
"""

FROM_EMAIL = "example@example.com"

SELECT_FILES_QUERY = "SELECT * FROM files WHERE hash = ?"
INSERT_FILE_QUERY = "INSERT INTO files (hash, timestamp) VALUES (?, ?)"
