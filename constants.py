BFI_URL = "https://www.bfi.org.uk/industry-data-insights/weekend-box-office-figures"

FILE_DOWNLOAD_LOCATION = "downloads/latest_report.xlsx"

BASE_HTML_TEMPLATE = "templates/_base.html"
TABLE_ROW_TEMPLATE = "templates/table_row.html"
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
