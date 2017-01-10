-- DATEBASE 생성
CREATE DATABASE scraping;

-- DATABASE 접근
USE scraping;

-- 테이블생성
CREATE TABLE keywords (
  id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
  keyword VARCHAR(64) NOT NULL
);

CREATE TABLE eng_keywords (
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
  UNIQUE INDEX idx1(section_id, keyword_id),
  FOREIGN KEY (keyword_id) REFERENCES keywords (id),
  FOREIGN KEY (section_id) REFERENCES sections (id)
);

CREATE TABLE eng_cnts (
  id INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY ,
  keyword_id INTEGER UNSIGNED NOT NULL ,
  section_id INTEGER UNSIGNED NOT NULL ,
  cnt INTEGER UNSIGNED DEFAULT 0,
  UNIQUE INDEX idx1(section_id, keyword_id),
  FOREIGN KEY (keyword_id) REFERENCES eng_keywords (id),
  FOREIGN KEY (section_id) REFERENCES sections (id)
);
-- // 테이블생성

SHOW INDEX FROM cnts;

ALTER DATABASE scraping CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE keywords CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE eng_keywords CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


SELECT character_set_name FROM information_schema.`COLUMNS` C
WHERE table_schema = "scraping"
  AND table_name = "keywords"
  AND column_name = "keyword";

SELECT character_set_name FROM information_schema.`COLUMNS` C
WHERE table_schema = "scraping"
  AND table_name = "eng_keywords"
  AND column_name = "keyword";

-- section 정보 insert
INSERT INTO sections(section)  values('COMPUTER');
INSERT INTO sections(section)  values('FASHION');

select * from eng_keywords
where 1>0
 and id in (176, 877)
;
select * from keywords
where 1>0
-- and id in (708,3)
and keyword='사용'
ORDER BY id ASC;

SELECT * FROM sections where section ='FASHION';
SELECT * FROM eng_cnts
where 1>0
  and keyword_id in (133)
ORDER BY cnt DESC;
SELECT * FROM cnts ORDER BY cnt DESC ;

-- table 정보 삭제
DELETE From eng_cnts
where keyword_id=877;
DELETE from eng_keywords;
COMMIT;



SELECT keyword_id, cnt FROM eng_cnts
WHERE section_id = 1
-- GROUP BY section_id
ORDER BY cnt DESC
 LIMIT 10
;