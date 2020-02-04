# -*- coding: utf-8 -*-
import mysql.connector
import json
from mysql.connector import Error
from .article import Article


class NewsRepo:
    conn = None

    def __init__(self):
        """ Connect to MySQL database """
        try:
            self.conn = mysql.connector.connect(host='localhost',
                                                database='news_db',
                                                user='root',
                                                password='12345678',
                                                charset='utf8')
            if self.conn.is_connected():
                print('Connected to MySQL database')

        except Error as e:
            print(e)

    def close_conn(self):
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()

    def insert_news(self, article):
        query = "insert into news (hashed_id, title, author, content, date, time, url, source) values (%s, %s, %s, %s, %s, %s, %s, %s)"
        args = (article.hashed_id, article.title, article.author, article.content,
                article.date, article.time, article.url, article.source)

        #cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, args)

            news_id = 0
            if cursor.lastrowid:
                #print('last insert id', cursor.lastrowid)
                news_id = cursor.lastrowid
            else:
                print('last insert id not found')

            self.conn.commit()

            for tag in article.tags:
                tag_id = self.insert_tag(tag)
                #print("tag_id: ", tag_id)
                self.insert_news_tag(news_id, tag_id)

        except Error as error:
            print(error)

        finally:
            cursor.close()

    def insert_tag(self, tag):
        query = "select * from tags where tag = %s"
        args = (tag, )

        #cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, args)

            row = cursor.fetchone()

            if row is not None:
                # print(row)
                return row[0]
            else:
                query = "insert into tags (tag) values (%s)"
                args = (tag, )

                cursor.execute(query, args)

                if cursor.lastrowid:
                    return cursor.lastrowid
                else:
                    print('last insert id not found')

                self.conn.commit()

        except Error as error:
            print(error)

        finally:
            cursor.close()

    def insert_news_tag(self, news_id, tag_id):
        query = "insert into news_tags (news_id, tag_id) values (%s, %s)"
        args = (news_id, tag_id)

        #cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, args)

            # if cursor.lastrowid:
            #     #print('last insert news_tag id', cursor.lastrowid)
            # else:
            #     print('last insert news_tag id not found')

            self.conn.commit()

        except Error as error:
            print(error)

        finally:
            cursor.close()

    def search_news_by_keyword(self, keyword):
        query = "select * from news where match (title, content, author) against (%s in natural language mode)"
        args = (keyword, )
        return self.get_articles(query, args)

    def search_news_by_tag(self, tag):
        query = "select * from news where id in (select news_id from news_tags where tag_id in (select id from tags where tag = %s))"
        args = (tag, )
        return self.get_articles(query, args)

    def get_articles(self, query, args):
        #cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, args)

            rows = cursor.fetchall()
            print('1 Total Row(s):', cursor.rowcount)
            articles = []

            for row in rows:
                article = Article()
                article.id = row[0]
                article.hashed_id = row[1]
                article.title = row[2]
                article.author = row[3]
                article.content = row[4]
                article.date = row[5]
                article.time = row[6]
                article.url = row[7]
                article.source = row[8]

                query = "select tag from tags where id in (select tag_id from news_tags where news_id = %s)"
                args = (article.id, )

                cursor.execute(query, args)

                tags = cursor.fetchall()

                article.tags = tags

                articles.append(article.__dict__)

            return articles

        except Error as error:
            print(error)

        finally:
            cursor.close()
