import json
from datetime import datetime
from flask import (
    render_template, session, jsonify, request, 
    abort, current_app, redirect, url_for, flash
)
from . import main
from .context import get_current_user
from .. import db
from ..models import Truck, User
from ..location import location_refresh



@main.route('/')
def home():
    return render_template('home.jinja')


@main.route('/data')
def data():
    trucks = Truck.get_trucks_with_geo()
    return jsonify({'trucks': trucks})


@main.route('/about')
def about():
    return render_template('about.jinja')


@main.route('/login')
def login():
    if 'logged_in' in session:
        return redirect(url_for('main.profile'))

    return render_template('login.jinja')


@main.route('/profile')
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('main.login'))

    user = get_current_user()
    return render_template('profile.jinja', user=user)


@main.route('/update', methods=['POST'])
def update():
    if 'logged_in' not in session:
        return json_fail('no_auth')

    user = get_current_user()

    if not user.truck:
        return json_fail('no_truck')

    post = request.form
    try:
        lat = round(float(post.get('lat')), 5)
        lng = round(float(post.get('lng')), 5)
        address = post.get('address')
    except Exception:
        return json_fail('parse_error')

    truck = user.truck

    truck.loc_lat = lat
    truck.loc_lng = lng
    truck.loc_display_address = address
    truck.loc_data = json.dumps([[lat, lng]])
    truck.loc_source = 'profile'
    truck.loc_updated = datetime.now()

    db.session.commit()

    return jsonify({'truck': truck.to_dict()})


@main.route('/trucks')
def trucks():
    trucks = Truck.query.order_by('display_name').all()
    return render_template('trucks.jinja', trucks=trucks)



# utilities

def json_fail(reason=None):
    return jsonify({
        'status': 'fail',
        'reason': reason
    })

