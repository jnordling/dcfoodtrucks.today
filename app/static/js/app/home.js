define([
    'jquery', 'underscore',
    'leaflet.pip', 'app/template',
    'mapbox', 'leaflet.markercluster', 'app/base'
], function($, _, leafletPip, tmpl) {

    // map setup

    L.mapbox.accessToken = 'pk.eyJ1IjoiYnJlbnN1ZG9sIiwiYSI6IjQxNDg2MjEwOTQ0OGU4ODc2YjIwYjZjMzVhMDlmN2JkIn0.ktzNWKCPYB20Kb1py_T5HA';

    var initial_zoom = $(window).width() > 500 ? 13 : 11;

    var map = L.mapbox.map('map', 'mapbox.streets', {
        zoomControl: false,
        minZoom: 10,
        maxZoom: 16
    }).setView([38.894, -77.030], initial_zoom);

    new L.Control.Zoom({
        position: 'bottomright',
        zoomInText: '<i class="fa fa-plus"></i>',
        zoomOutText: '<i class="fa fa-minus"></i>'
    }).addTo(map);


    // cluster layer setup

    var cluster_group = new L.MarkerClusterGroup({
        iconCreateFunction: function(cluster) {
            var count = cluster.getChildCount(),
                digits = (count + '').length;

            return new L.DivIcon({
                className: 'cluster digits-' + digits,
                html: count,
                iconSize: null
            });
        },
        showCoverageOnHover: false,
        zoomToBoundsOnClick: false,
        spiderfyOnMaxZoom: true,
        maxClusterRadius: 40,
        spiderfyDistanceMultiplier: 0.6
    });


    // fetch truck marker data

    var truck_layer = L.mapbox.featureLayer(),
        trucks = [],
        marker_active = false;

    var make_tooltip = function(data) {
        var shell = $('#truck-tt-tmpl').html(),
            tt = tmpl(shell, {
                data: data
            });
        return tt;
    };

    $.get('/data', function(response) {
        var data = response.trucks;

        data.forEach(function(d, i) {
            var loc = d.location || {};

            trucks.push({
                type: 'Feature',
                geometry: {
                    type: 'Point',
                    coordinates: [+loc.lng, +loc.lat]
                },
                properties: {
                    'marker-size': 'small',
                    'marker-color': '#d9534f',
                    title: make_tooltip(d),
                    info: d
                }
            });
        });


        truck_layer.setGeoJSON({
            type: 'FeatureCollection',
            features: trucks
        });


        cluster_group.addLayer(truck_layer);
        map.addLayer(cluster_group);
        get_trucks_in_view();
    });



    // events

    map.on('drag', function() {
        reset_highlight();
        get_trucks_in_view();
    });


    map.on('zoomend', function() {
        reset_highlight();
        get_trucks_in_view();
    });


    cluster_group.on('clusterclick', function(a) {
        set_highlight(a.layer, 'cluster');

        var children = a.layer.getAllChildMarkers(),
            trucks = [];

        children.forEach(function(c) {
            trucks.push(c.feature.properties.info);
        });

        // a.layer.zoomToBounds();
        // a.layer.spiderfy();
        update_truck_list(trucks, 'cluster');
        off_canvas_list.show();
    });


    truck_layer.on('click', function(e) {
        set_highlight(e.layer, 'pt');
        e.layer.openPopup();

        var truck = e.layer.feature.properties.info;
        update_truck_list([truck], 'marker');
    });



    // set/remove active state to markers

    function set_highlight(layer, type) {
        reset_highlight();

        if (type == 'cluster') {
            $(layer._icon).addClass('active');
        } else if (type == 'pt') {
            layer.setIcon(L.mapbox.marker.icon({
                'marker-color': '#000',
                'marker-size': 'small'
            }));
        }

        marker_active = true;
    }


    function reset_highlight() {
        if (marker_active) {
            map.closePopup();

            $('.cluster').removeClass('active');

            truck_layer.eachLayer(function(layer) {
                layer.setIcon(L.mapbox.marker.icon({
                    'marker-color': '#d9534f',
                    'marker-size': 'small'
                }));
            });

            marker_active = false;
        }
    }


    // off canvas (bottom) truck list (for mobile devices)

    $('body').on('click', '#trucks-ct', function(e) {
        e.preventDefault();
        off_canvas_list.toggle();
    });

    var off_canvas_list = {
        btn: $('#trucks-ct'),
        body: $('body'),
        cls: 'off-canvas-visible',

        is_visible: function() {
            return this.body.hasClass(this.cls);
        },

        truck_ct: function() {
            return this.btn.data('ct');
        },

        show: function() {
            this.body.addClass(this.cls);
            this.btn.addClass('close-ico');
            this.btn.text('×');
        },

        hide: function() {
            this.body.removeClass(this.cls);
            this.btn.text(this.truck_ct());
        },

        toggle: function(state) {
            this.is_visible() ? this.hide() : this.show();
        }
    };



    // filter to trucks within viewport

    function get_trucks_in_view() {
        var trucks_in_view = [],
            bounds = map.getBounds();

        truck_layer.eachLayer(function(marker) {
            if (bounds.contains(marker.getLatLng())) {
                var truck = marker.feature.properties.info;
                trucks_in_view.push(truck);
            }
        });

        update_truck_list(trucks_in_view);
    }


    // display list of trucks in view

    function update_truck_list(trucks, context) {
        update_truck_ct_btn(trucks.length);

        trucks = _.sortBy(trucks, 'name');

        var subset = trucks.slice(0, 30);
        subset = _.uniq(subset, function(t) {
            return t.name;
        });

        var shell = $('#truck-list-tmpl').html(),
            html = tmpl(shell, {
                data: subset,
                context: context || 'normal',
                truck_ct: trucks.length
            });

        $('.trucks-in-view').empty().append(html);
    }


    function update_truck_ct_btn(ct) {
        var btn = $('#trucks-ct');

        btn.removeClass('close-ico');
        btn.text(ct);
        btn.data('ct', ct);
    }


    // geolocation functionality

    var geolocate = $('#geolocator'),
        meLayer = L.mapbox.featureLayer().addTo(map);

    if (!navigator.geolocation) {
        console.log('Geolocation is not available');
    } else {
        geolocate.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            geolocate.button('loading');
            map.locate();
        });
    }


    map.on('locationfound', function(e) {
        map.fitBounds(e.bounds, {
            maxZoom: 15
        });

        meLayer.setGeoJSON({
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [e.latlng.lng, e.latlng.lat]
            },
            properties: {
                'title': 'Me!',
                'marker-color': '#0071dc',
                'marker-symbol': 'star'
            }
        });

        geolocate.button('reset');
    });


    map.on('locationerror', function(e) {
        geolocate.button('reset');
        alert('Bummer. Your location could not be found :(');
    });

});
