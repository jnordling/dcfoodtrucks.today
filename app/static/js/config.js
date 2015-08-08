;(function() {
  requirejs.config({
    baseUrl: '/static/js',
    waitSeconds: 20,

    paths: {
      requireLib: 'lib/require',

      async: 'lib/async',

      jquery: 'lib/jquery.min',
      'jquery.cookie': 'lib/jquery.cookie',
      'jquery.querystring': 'lib/jquery.querystring',
      'jquery.geocomplete': 'lib/jquery.geocomplete.min',
      
      typeahead: 'lib/typeahead.bundle.min',

      underscore: 'lib/underscore-min',
      bootstrap: 'lib/bootstrap.min',
      moment: 'lib/moment.min',

      d3: 'lib/d3.v3.min',
      'd3.geo': 'lib/d3.geo.projection.v0.min',

      topojson: 'lib/topojson.v1.min',
      queue: 'lib/queue.min',

      leaflet: 'lib/leaflet',
      'leaflet.pip': 'lib/leaflet-pip',
      'leaflet.markercluster': 'lib/leaflet.markercluster',

      mapbox: 'lib/mapbox',

      pikabu: 'lib/pikabu.min'
    },

    shim: {
      bootstrap: {
        deps: ['jquery'],
        exports: '$.fn.popover'
      },
      'typahead': { deps: ['jquery'] },
      'jquery.geocomplete': { deps: ['jquery'] },
      'leaflet.pip': { deps: ['leaflet'] },
      'leaflet.markercluster': { deps: ['mapbox', 'leaflet'] },
      'mapbox': { deps: ['leaflet'] }
    }

  });
})();
