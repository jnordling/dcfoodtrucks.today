from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
from config import config


db = SQLAlchemy()
oauth = OAuth()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    oauth.init_app(app)

    app.tw_oauth = oauth.remote_app(
        'twitter',
        base_url='https://api.twitter.com/1.1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key=app.config['TWITTER_CONSUMER_KEY'],
        consumer_secret=app.config['TWITTER_CONSUMER_SECRET']
    )
    @app.tw_oauth.tokengetter
    def get_tw_token():
        return session.get('twitter_token')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
