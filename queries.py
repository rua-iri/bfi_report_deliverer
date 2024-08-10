SELECT_USERS_QUERY = """
SELECT *
FROM users
WHERE is_active = TRUE;
"""

CREATE_USERS_TABLE_QUERY = """
CREATE TABLE "users" (
"id"	INTEGER,
"first_name"	TEXT,
"last_name"	TEXT,
"email"	TEXT,
"is_active"	BOOL,
PRIMARY KEY("id")
);
"""

CREATE_FILES_TABLE_QUERY = """
CREATE TABLE "files" (
"id"	INTEGER,
"hash"	TEXT,
"timestamp"	INTEGER,
PRIMARY KEY("id" AUTOINCREMENT)
);
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
