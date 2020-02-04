# News Crawler

News Crawler is a simple python project which extracts latest news from [yallakora.com](https://yallakora.com), store them MYSQL DB and expose 2 APIs to search the news.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install news-crawler.

```bash
pip install -r requirements.txt
```

Import DB schema in file `schema.sql`

Change DB credentials in file `./scrapper/models/news_repo.py`

## Usage

#### Extract news data from yallakora

```bash
scrapy crawl yallakora
```

#### Run flask

```bash
export FLASK_APP=main.py
flask run
```

## REST APIs

There are 2 APIs provided

### Search news by keyword

#### Request

`GET /api/json/news/<keyword>`

    curl -i http://localhost:5000/api/json/news/<keyword>

### Search news by tag

#### Request

`GET /api/json/tags/<keyword>`

    curl -i http://localhost:5000/api/json/tags/<keyword>
