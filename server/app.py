#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

   articles = Article.query.all()
   article_list = [article.to_dict() for article in articles]

   return jsonify(article_list)

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize the session value if not already set
    session['page_views'] = session.get('page_views',0)

    #Increment the page view count
    session['page_views'] += 1

    #Check if user has exceeded view limit
    if session['page_views'] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401
    
    # Fetch the article data from the database
    article = Article.query.filter_by(id=id).first()
    if article:
        article_resp = article.to_dict()
        return make_response(jsonify(article_resp))
    else:
        return jsonify({'message': 'Article not found'}), 404



if __name__ == '__main__':
    app.run(port=5555)
