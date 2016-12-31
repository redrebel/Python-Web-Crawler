DB 는 Mysql.
개발환경은 Docker를 이용. 

### sections (분야테이블)
컬럼 | 타입(사이즈) | 기타
---- | ---------- | ----
id  | INTEGER | PK
section | VARCHAR(64) | NOT NULL

### keywords (단어테이블)
컬럼 | 타입(사이즈) | 기타
---- | ---------- | ----
id  | INTEGER | PK
keyword | VARCHAR(64) | NOT NULL

### cnts (빈도수테이블)
컬럼 | 타입(사이즈) | 기타
---- | ---------- | ----
id  | INTEGER | PK
keyword_id | INTEGER | FK(keywords id)
section_idx | INTEGER | FK(sections idx)
cnt | INTEGER | 0

### eng_keywords (단어테이블)
컬럼 | 타입(사이즈) | 기타
---- | ---------- | ----
id  | INTEGER | PK
keyword | VARCHAR(64) | NOT NULL

### eng_cnts (빈도수테이블)
컬럼 | 타입(사이즈) | 기타
---- | ---------- | ----
id  | INTEGER | PK
keyword_id | INTEGER | FK(eng_keywords id)
section_idx | INTEGER | FK(sections idx)
cnt | INTEGER | 0