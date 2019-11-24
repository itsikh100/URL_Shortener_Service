DROP TABLE IF EXISTS URL;

CREATE TABLE URL (
  shortUrl TEXT UNIQUE NOT NULL,
  longUrl TEXT NOT NULL,
  modifyTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);