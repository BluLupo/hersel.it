#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright Hersel Giannella

from database.connection import Database
from database.models.articles import Article
from sqlalchemy import text

db = Database()
session = db.Session()

def get_article_by_id(article_id):
    try:
        # Esegui una query SQLAlchemy per ottenere l'articolo per ID
        article = session.query(Article).filter_by(id=article_id).first()

        if article:
            # Converte l'oggetto Article in un dizionario
            article_dict = {column.name: getattr(article, column.name) for column in Article.__table__.columns}
            return article_dict
        else:
            return None
    finally:
        session.close()


def get_articles_and_authors_raw():
    try:
        query = text("SELECT art.id as articleid,art.title,art.content,art.created_at,art.updated_at,art.photo_article,art.publish_status,u.id as userid,u.username FROM articles art INNER JOIN users u ON art.author_id = u.id WHERE art.publish_status = 1")
        result = session.execute(query)

        # Utilizza il metodo keys() per ottenere i nomi delle colonne
        column_names = result.keys()

        # Cicla su result per ottenere tutti i risultati come dizionari
        result_list = [dict(zip(column_names, row)) for row in result]

        return result_list
    finally:
        session.close()

def create_article(title, content, author_id, photo_article):
    try:
        new_article = Article(title=title, content=content, author_id=author_id, photo_article=photo_article)
        session.add(new_article)
        session.commit()
    except Exception as e:
        print(f"Error creating article: {e}")
        session.rollback()  # Rollback the transaction in case of an error
    finally:
        session.close()
