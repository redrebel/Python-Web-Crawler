# Python-Web-Crawler
Python으로 만드는 웹크롤러

인터넷에서 등록되어있는 블로그나 기사를 크롤링하여 한글 말뭉치를 이용하여 명사단어
를 추출하여 그 사용 빈도수를 저장한다.
부가적으로 TEXT 파일포맷의 파일을 파싱하여 같은 방법으로 빈도수를 저장한다. 
 
1. egloos 에 등록된 글을 읽어와서 단어를 추출한후  DB에 등록
1. 다른 블로그들도 추가
2. 이미 scraping 되서서 text 포맷으로 저장된 파일을 열어서 단어를 추출한후 DB에 저장

사용파이썬 패키지
- [KoNLPy: 파이썬 한국어 NLP](http://konlpy.org/ko/latest/)
    - Kkma 는 nouns() 시 단어를 한번만 표시되고 속도가 느리지만 추출결과가 깔끔하다
    - Hannanum 은 nouns() 시 단어를 매번 표시되고 (빈도수체크가능) 속도가 빠르지만 추출결과가 매끄럽지 않다.
    
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
    - pip3 install BeautifulSoup4
    
- [lxml]()
    - pip3 install lxml

기타
- [Docker](https://docs.docker.com/engine/installation/mac/)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)