-- DATEBASE 생성
CREATE DATABASE scraping;

-- DATABASE 접근
USE scraping;

-- 테이블생성
CREATE TABLE keywords (
  id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
  keyword VARCHAR(64) NOT NULL
);

CREATE TABLE sections (
  id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  section VARCHAR(64) NOT NULL
);

CREATE TABLE cnts (
  id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
  keyword_id INTEGER UNSIGNED NOT NULL ,
  section_id INTEGER UNSIGNED NOT NULL ,
  cnt INTEGER UNSIGNED DEFAULT 0,
  UNIQUE INDEX idx1(keyword_id),
  FOREIGN KEY (keyword_id) REFERENCES keywords (id),
  FOREIGN KEY (section_id) REFERENCES sections (id)
);

SHOW INDEX FROM cnts;

ALTER DATABASE scraping CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE keywords CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


SELECT character_set_name FROM information_schema.`COLUMNS` C
WHERE table_schema = "scraping"
  AND table_name = "keywords"
  AND column_name = "keyword";

