define([
    'async!https://maps.googleapis.com/maps/api/js?libraries=places&sensor=false',
    'jquery', 'underscore', 'profile_config',
    'jquery.geocomplete', 'mapbox', 'app/base'
], function(gmap, $, _, config) {


    var user = config.user,
        truck = config.truck_info,  
        map, marker;


    if (user.has_truck) {
        map_init();
        if (config.has_location) {
            var loc = config.truck_location;
            add_marker([loc.lng, loc.lat]);
        }
    }


    function map_init() {
        L.mapbox.accessToken = 'pk.eyJ1IjoiYnJlbnN1ZG9sIiwiYSI6IjQxNDg2MjEwOTQ0OGU4ODc2YjIwYjZjMzVhMDlmN2JkIn0.ktzNWKCPYB20Kb1py_T5HA';

        var center = [38.8934, -77.0322],
            zoom = 11;

        if (config.has_location) {
            var loc = config.truck_location;
            center = [loc.lat, loc.lng];
            zoom = 14;
        }

        map = L.mapbox.map('profile-map', 'mapbox.streets', {
            zoomControl: false
        }).setView(center, zoom);

        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        map.scrollWheelZoom.disable();
    }


    function add_marker(coordinates, go_to_pt) {
        if (marker) map.removeLayer(marker);

        marker = L.mapbox.featureLayer({
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: coordinates
            },
            properties: {
                title: truck.name || '',
                'marker-color': '#d9524d',
            }
        }).addTo(map);

        if (go_to_pt) {
            map.fitBounds(marker.getBounds(), {maxZoom: 14});
        }
    }



    //////////////////////////////////////////////
    //////////////////////////////////////////////



    function geo_success(result) {
        var form = $('#geo-form'),
            formatted_address = result.formatted_address,
            location = result.geometry.location,
            lat = location.lat(),
            lng = location.lng();

        form.find('input[name="address"]').val(formatted_address);
        form.find('input[name="lat"]').val(lat);
        form.find('input[name="lng"]').val(lng);

        add_marker([lng, lat], true);
    }


    function geo_fail(status) {
        console.log("ERROR: " + status);
    }


    function geocomplete_init() {
        $(".geocomplete").geocomplete()
            .bind("geocode:result", function(e, result) { geo_success(result); })
            .bind("geocode:error", function(e, status) { geo_fail(status); })
            .bind("geocode:multiple", function(e, results) { geo_success(results[0]); });
    }

    geocomplete_init();




    //////////////////////////////////////////////
    //////////////////////////////////////////////



    $("#geo-form").submit(function(e) {
        e.preventDefault();
        LocationForm.submit();
    });


    var LocationForm = {
        form: $("#geo-form"),
        btn: $("#geo-submit"),
        alert: $("#geo-alert"),
        data: null,


        submit: function() {
            this.loading();
            this.get_data();
            if (this.validate() === true) this.post();
        },


        loading: function() {
            this.btn.button("loading");
            this.alert.addClass("hidden");
        },


        get_data: function() {
            this.data = this.form.form_data_obj();
        },


        validate: function() {
            var d = this.data;

            if (d.lat === "") {
                this.fail("Please enter a valid address.");
                return;
            }

            return true;
        },


        post: function() {
            var endpoint = this.form.attr("action"),
                post_data = this.data,
                self = this;

            var posting = $.post(endpoint, post_data, 'json');

            posting.done(function(response) {
                console.log(response);

                if (response.status == 'fail') {
                    self.fail();
                } else {
                    self.success(response);
                }
            });

            posting.fail(function() {
                self.fail();
            });
        },


        fail: function(msg) {
            if (!msg) msg = "Something went wrong :(";

            this.alert.find(".msg").text(msg);
            this.alert.removeClass("hidden");
            this.btn.button("reset");
        },


        success: function(response) {
            this.alert.find(".msg").text("Success! Location updated :)");
            this.alert.removeClass("hidden");
            this.btn.button('reset');
        }
    };


});
