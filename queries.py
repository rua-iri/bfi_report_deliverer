SELECT_USERS_QUERY = """
SELECT *
FROM users
WHERE is_active = TRUE;
"""

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

SELECT_FILES_QUERY = """SELECT *
FROM files
WHERE hash = ?
"""

INSERT_FILE_QUERY = """
INSERT INTO files
(hash, timestamp)
VALUES (?, ?)
"""
