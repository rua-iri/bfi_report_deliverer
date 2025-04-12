
import sqlite3
from bfi_report_deliverer.queries import (
    CREATE_USERS_TABLE_QUERY,
    CREATE_FILES_TABLE_QUERY
)


con = sqlite3.connect("bfi_report.db")
con.row_factory = sqlite3.Row


def create_db():
    """Create users & files table in database
    (should only run on initialising repository)
    """
    cursor = con.cursor()
    res = cursor.execute(CREATE_USERS_TABLE_QUERY)
    res.fetchall()
    cursor = con.cursor()
    res = cursor.execute(CREATE_FILES_TABLE_QUERY)
    res.fetchall()


def main():
    create_db()
    print("Database Initialised Successfully")


if __name__ == "__main__":
    main()
