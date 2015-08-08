import json
import twitter
import calendar
import time
from pytz import timezone
from datetime import datetime
from flask import current_app
from sqlalchemy import and_, or_
from . import db



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    tw_user_id = db.Column(db.String(64))
    tw_oauth_token = db.Column(db.String(256))
    tw_oauth_secret = db.Column(db.String(256))

    email = db.Column(db.String(128))
    username = db.Column(db.String(64))
    name = db.Column(db.String(128))
    avatar = db.Column(db.String(512))

    create_date = db.Column(db.DateTime, default=db.func.now())
    update_date = db.Column(db.DateTime, default=db.func.now())

    truck = db.relationship('Truck', backref='user', uselist=False)


    def __repr__(self):
        return '<User %r>' % self.username


    @property
    def has_truck(self):
        return True if self.truck else False


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'avatar': self.avatar,
            'has_truck': self.has_truck,
        }



class Truck(db.Model):
    __tablename__ = 'trucks'
    id = db.Column(db.Integer, primary_key=True)

    display_name = db.Column(db.String(256))

    tw_handle = db.Column(db.String(128))
    website = db.Column(db.String(256))

    img_thumb = db.Column(db.String(512))

    create_date = db.Column(db.DateTime, default=db.func.now())
    update_date = db.Column(db.DateTime, default=db.func.now())

    last_tweet_id = db.Column(db.String(32))
    last_tweet_time = db.Column(db.DateTime)
    last_tweet_text = db.Column(db.String(256))

    loc_lat = db.Column(db.Numeric)
    loc_lng = db.Column(db.Numeric)
    loc_display_address = db.Column(db.String(256))
    loc_source = db.Column(db.String(64))
    loc_updated = db.Column(db.DateTime)

    loc_data = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __repr__(self):
        return '<Truck %r>' % self.id


    def to_dict(self):
        return {
            'id': self.id,
            'handle': self.tw_handle,
            'name': self.display_name,
            'img': self.thumb_lg,
            'last_tweet': self.last_tweet,
            'loc_updated': self.loc_updated,
        }


    @property
    def last_tweet(self):
        data = {
            'text': self.last_tweet_text,
            'date': self.last_tweet_time,
        }

        if self.last_tweet_time:
            data['epoch'] = utc_dt_to_seconds(self.last_tweet_time)
            data['date_display'] = self.last_tweet_time_display

        return data


    @property
    def last_tweet_time_display(self):
        if not self.last_tweet_time:
            return

        utc = timezone('UTC')
        eastern = timezone('US/Eastern')

        dt = self.last_tweet_time
        loc_dt = dt.replace(tzinfo=utc).astimezone(eastern)

        fmt = '%B %-d, %Y, %-I:%M %p'
        return loc_dt.strftime(fmt)


    @property
    def thumb_lg(self):
        if not self.img_thumb:
            return

        return self.img_thumb.replace('_normal.', '_400x400.')


    @property
    def truck_ct(self):
        trucks = self.locations

        if not trucks:
            return 0

        return len(trucks)


    @property
    def has_location(self):
        return True if self.loc_lat else False


    @property
    def location(self):
        if not self.loc_lat:
            return

        return {
            'lat': self.loc_lat,
            'lng': self.loc_lng,
            'updated': self.loc_updated,
        }


    @property
    def locations(self):
        if not self.loc_data:
            return

        try:
            locations = json.loads(self.loc_data)
        except Exception:
            return

        return locations


    @staticmethod
    def add_truck(name, handle):
        truck = Truck.query.filter_by(tw_handle=handle).first()

        if truck:
            print 'already exists'
            return

        truck = Truck(
            display_name = name,
            tw_handle = handle,
        )
        db.session.add(truck)
        db.session.commit()
        print 'added!'


    @staticmethod
    def load_trucks():
        with open('app/static/data/trucks.json') as infile:
            data = json.load(infile)

        new_peeps, old_peeps, no_tw = 0, 0, 0

        for d in data:
            tw = None if len(d['tw_handle']) == 0 else d['tw_handle'].lower()
            website = None if len(d['website']) == 0 else d['website']

            if tw:
                truck = Truck.query.filter_by(tw_handle = tw).first()

                if truck is None:
                    truck = Truck(
                        display_name = d['name'],
                        tw_handle = tw,
                        website = website,
                    )
                    db.session.add(truck)
                    db.session.commit()
                    new_peeps += 1
                else:
                    old_peeps += 1
            else:
                no_tw += 1

        print 'new peeps: %d' % new_peeps
        print 'old peeps: %d' % old_peeps
        print 'no twitter accounts: %d' % no_tw


    @staticmethod
    def twitter_refresh():
        tw = _tw_api()

        trucks = Truck.query.all()
        truck_chunks = _chunks(trucks, 50)

        print '%d total chunks' % len(truck_chunks)
        timeline_fetches = 0

        for truck_chunk in truck_chunks:
            handles = [t.tw_handle for t in truck_chunk]
            tw_results = tw.UsersLookup(screen_name=handles)

            print '%d hits out of %d' % (len(tw_results), len(handles))

            for result in tw_results:
                handle = result.screen_name.lower()
                truck = Truck.query.filter_by(tw_handle = handle).first()

                truck.img_thumb = result.profile_image_url

                tweet = result.status
                if tweet:
                    txt = tweet.text
                    if len(txt) < 2 or txt[0] == '@' or txt[:2] == 'RT':
                        timeline_fetches += 1
                        tweets = tw.GetUserTimeline(
                            screen_name=handle, 
                            exclude_replies=True, 
                            include_rts=False, 
                            count=50
                        )
                        if len(tweets) > 0:
                            tweet = tweets[0]
                    truck.last_tweet_id = tweet.id
                    truck.last_tweet_time = datetime.fromtimestamp(tweet.created_at_in_seconds)
                    truck.last_tweet_text = tweet.text
            db.session.commit()
            print 'timeline fetches: %d' % timeline_fetches


    @staticmethod
    def get_trucks_by_handle():
        trucks = Truck.query.all()

        results = {}
        for truck in trucks:
            results[truck.tw_handle] = {
                'obj': truck,
                'data': truck.to_dict(),
            }

        return results


    @staticmethod
    def get_trucks_with_geo():
        trucks = Truck.query\
            .filter(Truck.loc_lat != None)\
            .all()

        results = []
        for t in trucks:
            if t.locations:
                for l in t.locations:
                    entry = t.to_dict()
                    entry['location'] = {'lat': l[0], 'lng': l[1]}
                    results.append(entry)

        blacklist = ['brensudol']
        results = [r for r in results if r.get('handle') not in blacklist]

        return results


    @staticmethod
    def clear_locations():
        trucks = db.session.query(Truck)\
            .filter(Truck.loc_lat != None)\
            .filter(or_(
                Truck.loc_source == None, 
                Truck.loc_source != 'profile',
            ))

        ct = trucks.count()

        if ct > 0:
            trucks.update({
                'loc_lat': None,
                'loc_lng': None,
                'loc_source': None,
                'loc_updated': None,
                'loc_data': None,
            })
            db.session.commit()

        return {'ct': ct}



# misc, utility functions

def _tw_api():
    return twitter.Api(
        consumer_key = current_app.config['TWITTER_CONSUMER_KEY'],
        consumer_secret = current_app.config['TWITTER_CONSUMER_SECRET'],
        access_token_key = current_app.config['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret = current_app.config['TWITTER_ACCESS_TOKEN_SECRET'],
    )


def _chunks(l, n):
    return [l[i:i+n] for i in xrange(0, len(l), n)]


def utc_dt_to_seconds(dt):
    return calendar.timegm(dt.timetuple())

