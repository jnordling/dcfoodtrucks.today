from flask import render_template, redirect, request, url_for, flash, current_app, session
from flask_oauthlib.client import OAuthException
from . import auth
from .. import db
from ..models import Truck, User



@auth.route('/tw')
def tw_auth():
    tw = current_app.tw_oauth
    callback = url_for(
        'auth.tw_auth_callback',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    )
    return tw.authorize(callback=callback)



@auth.route('/tw/authorized')
def tw_auth_callback():
    tw = current_app.tw_oauth
    next_url = request.args.get('next') or url_for('main.home')
    resp = tw.authorized_response()
    print resp

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    oauth_token = resp.get('oauth_token')
    oauth_token_secret = resp.get('oauth_token_secret')
    tw_id = resp.get('user_id')
    tw_handle = resp.get('screen_name')

    # store oauth info in session    
    session['logged_in'] = True
    session['twitter_token'] = (
        oauth_token, 
        oauth_token_secret
    )

    # get more twitter user info
    tw_response = tw.get('account/verify_credentials.json?include_email=true')
    tw_data = tw_response.data if tw_response.status == 200 else {}
    email = tw_data.get('email')
    name = tw_data.get('name')
    avatar = tw_data.get('profile_image_url_https')

    # maybe add user to db
    user = User.query.filter_by(tw_user_id = tw_id).first()
    if user is None:
        user = User(
            tw_user_id = tw_id,
            tw_oauth_token = oauth_token,
            tw_oauth_secret = oauth_token_secret,
            email=email,
            username=tw_handle,
            name=name,
            avatar=avatar,
        )
        db.session.add(user)
        db.session.commit()

        # check for truck
        truck = Truck.query.filter_by(
            tw_handle = tw_handle.lower()
        ).first()
        if truck:
            user.truck = truck
            db.session.commit()

        flash('Welcome @%s!' % tw_handle, 'good')
    else:
        # update img (just in case)
        user.avatar = avatar
        db.session.commit()

    session['user'] = user.to_dict()
    return redirect(url_for('main.profile'))



@auth.route("/logout")
def logout():
    pop_login_session()
    return redirect(url_for('main.home'))



def pop_login_session():
    session.pop('logged_in', None)
    session.pop('twitter_token', None)
    session.pop('user', None)

