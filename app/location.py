import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
from operator import itemgetter
from . import db
from .models import Truck



def location_refresh():
    url = 'http://foodtruckfiesta.com/apps/map_json.php' + \
        '?num_days=365&minimal=0&alert_nc=y&alert_hc=0&alert_pm=0&rand=1'
    
    try:
        response = json.loads(requests.get(url, timeout=10).content)
        markers = response.get('markers')
    except Exception:
        markers = []

    print 'Number of truck locations found: %d' % len(markers)

    # cluster markers by proximity
    markers = _cluster_markers(markers)

    # get trucks from db
    trucks = Truck.get_trucks_by_handle()

    # clear current locations
    if len(markers) > 0:
        Truck.clear_locations()

    results = defaultdict(int)
    locs_by_truck = defaultdict(list)

    for marker in markers:
        handle = marker.get('truck', '').lower()
        truck = trucks.get(handle)

        if not truck:
            results['errors'] += 1
            continue

        t = truck['obj']

        if t.loc_source == 'profile':
            results['profile_pass'] += 1
            continue

        lat = marker.get('lat_adj')
        lng = marker.get('lng_adj')
        locs_by_truck[handle].append([lat, lng])

        t.loc_lat = lat
        t.loc_lng = lng
        t.loc_source = 'script'
        t.loc_updated = datetime.now()
        results['successes'] += 1

    for handle, locations in locs_by_truck.iteritems():
        t = trucks.get(handle)['obj']
        t.loc_data = json.dumps(locations)

    db.session.commit()
    print dict(results)



def _cluster_markers(markers, threshold=0.00025):
    # convert lat, lng to numbers
    data = []
    for marker in markers:
        try:
            marker['lat'] = float(marker['coord_lat'])
            marker['lng'] = float(marker['coord_long'])
            data.append(marker)
        except Exception:
            pass

    # sort by lat
    data = sorted(data, key=itemgetter('lat'))

    # create adjusted lat, lng based on prior markers
    prev = {'lat': 0, 'lng': 0}
    clusters = defaultdict(int)

    for i, d in enumerate(data):
        d['lat_adj'] = d['lat']
        d['lng_adj'] = d['lng']
        d['cluster_base'] = d['print_name']

        if (d['lat'] - prev['lat']) < threshold:
            matches = [
                d2 for d2 in data[:i] if 
                (d['lat'] - d2['lat']) < threshold and
                (d['lng'] - d2['lng']) < threshold and 
                (d['lng'] - d2['lng']) > 0
            ]

            if len(matches) > 0:
                match = matches[0]
                d['lat_adj'] = match['lat_adj']
                d['lng_adj'] = match['lng_adj']
                d['cluster_base'] = match['cluster_base']
                clusters[match['cluster_base']] += 1

        prev = d

    return data
