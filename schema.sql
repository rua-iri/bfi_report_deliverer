CREATE TABLE users
(
id INTEGER PRIMARY KEY,
first_name TEXT,
last_name TEXT,
email TEXT,
is_active BOOL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "files" (
	"id"	INTEGER,
	"hash"	TEXT,
	"timestamp"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
