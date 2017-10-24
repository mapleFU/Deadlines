(function() {
    var AdminForm = function() {
      // Field converters
      var fieldConverters = [];

      /**
      * Process AJAX fk-widget
      */
      function processAjaxWidget($el, name) {
        var multiple = $el.attr('data-multiple') == '1';

        var opts = {
          width: 'resolve',
          minimumInputLength: 1,
          placeholder: 'data-placeholder',
          ajax: {
            url: $el.attr('data-url'),
            data: function(term, page) {
              return {
                query: term,
                offset: (page - 1) * 10,
                limit: 10
              };
            },
            results: function(data, page) {
              var results = [];

              for (var k in data) {
                var v = data[k];

                results.push({id: v[0], text: v[1]});
              }

              return {
                results: results,
                more: results.length == 10
              };
            }
          },
          initSelection: function(element, callback) {
            $el = $(element);
            var value = jQuery.parseJSON($el.attr('data-json'));
            var result = null;

            if (value) {
              if (multiple) {
                result = [];

                for (var k in value) {
                  var v = value[k];
                  result.push({id: v[0], text: v[1]});
                }

                callback(result);
              } else {
                result = {id: value[0], text: value[1]};
              }
            }

            callback(result);
          }
        };

        if ($el.attr('data-allow-blank'))
          opts['allowClear'] = true;

        opts['multiple'] = multiple;

        $el.select2(opts);
      }

      /**
       * Process Leaflet (map) widget
       */
      function processLeafletWidget($el, name) {
        if (!window.MAPBOX_MAP_ID) {
          console.error("You must set MAPBOX_MAP_ID in your Flask settings to use the map widget");
          return false;
        }

        var geometryType = $el.data("geometry-type")
        if (geometryType) {
          geometryType = geometryType.toUpperCase();
        } else {
          geometryType = "GEOMETRY";
        }
        var multiple = geometryType.lastIndexOf("MULTI", geometryType) === 0;
        var editable = ! $el.is(":disabled");

        var $map = $("<div>").width($el.data("width")).height($el.data("height"));
        $el.after($map).hide();

        var center = null;
        if($el.data("lat") && $el.data("lng")) {
          center = L.latLng($el.data("lat"), $el.data("lng"));
        }

        var maxBounds = null;
        if ($el.data("max-bounds-sw-lat") && $el.data("max-bounds-sw-lng") &&
          $el.data("max-bounds-ne-lat") && $el.data("max-bounds-ne-lng"))
        {
          maxBounds = L.latLngBounds(
            L.latLng($el.data("max-bounds-sw-lat"), $el.data("max-bounds-sw-lng")),
            L.latLng($el.data("max-bounds-ne-lat"), $el.data("max-bounds-ne-lng"))
          )
        }

        var editableLayers;
        if ($el.val()) {
          editableLayers = new L.geoJson(JSON.parse($el.val()));
          center = center || editableLayers.getBounds().getCenter();
        } else {
          editableLayers = new L.geoJson();
        }

        var mapOptions = {
          center: center,
          zoom: $el.data("zoom") || 12,
          minZoom: $el.data("min-zoom"),
          maxZoom: $el.data("max-zoom"),
          maxBounds: maxBounds
        }

        if (!editable) {
          mapOptions.dragging = false;
          mapOptions.touchzoom = false;
          mapOptions.scrollWheelZoom = false;
          mapOptions.doubleClickZoom = false;
          mapOptions.boxZoom = false;
          mapOptions.tap = false;
          mapOptions.keyboard = false;
          mapOptions.zoomControl = false;
        }

        // only show attributions if the map is big enough
        // (otherwise, it gets in the way)
        if ($map.width() * $map.height() < 10000) {
          mapOptions.attributionControl = false;
        }

        var map = L.map($map.get(0), mapOptions)
        map.addLayer(editableLayers);

        if (center) {
          // if we have more than one point, make the map show everything
          var bounds = editableLayers.getBounds()
          if (!bounds.getNorthEast().equals(bounds.getSouthWest())) {
            map.fitBounds(bounds);
          }
        } else {
          // look up user's location by IP address
          $.getJSON("//ip-api.com/json/?callback=?", function(data) {
            map.setView([data["lat"], data["lon"]], 12);
          }).fail(function() {
              map.setView([0, 0], 1)
          });
        }

        // set up tiles
        var mapboxVersion = window.MAPBOX_ACCESS_TOKEN ? 4 : 3;
        L.tileLayer('//{s}.tiles.mapbox.com/v'+mapboxVersion+'/'+MAPBOX_MAP_ID+'/{z}/{x}/{y}.png?access_token='+window.MAPBOX_ACCESS_TOKEN, {
          attribution: 'Map data &copy; <a href="//openstreetmap.org">OpenStreetMap</a> contributors, <a href="//creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="//mapbox.com">Mapbox</a>',
          maxZoom: 18
        }).addTo(map);


        // everything below here is to set up editing, so if we're not editable,
        // we can just return early.
        if (!editable) {
          return true;
        }

        // set up Leaflet.draw editor
        var drawOptions = {
          draw: {
            // circles are not geometries in geojson
            circle: false
          },
          edit: {
            featureGroup: editableLayers
          }
        }

        if ($.inArray(geometryType, ["POINT", "MULTIPOINT"]) > -1) {
          drawOptions.draw.polyline = false;
          drawOptions.draw.polygon = false;
          drawOptions.draw.rectangle = false;
        } else if ($.inArray(geometryType, ["LINESTRING", "MULTILINESTRING"]) > -1) {
          drawOptions.draw.marker = false;
          drawOptions.draw.polygon = false;
          drawOptions.draw.rectangle = false;
        } else if ($.inArray(geometryType, ["POLYGON", "MULTIPOLYGON"]) > -1) {
          drawOptions.draw.marker = false;
          drawOptions.draw.polyline = false;
        }
        var drawControl = new L.Control.Draw(drawOptions);
        map.addControl(drawControl);
        if (window.MAPBOX_SEARCH) {
          var circle = L.circleMarker([0, 0]);
          var $autocompleteEl = $('<input style="position: absolute; z-index: 9999; display: block; margin: -42px 0 0 10px; width: 50%">');
          var $form = $($el.get(0).form);

          $autocompleteEl.insertAfter($map);
          $form.on('submit', function (evt) {
            if ($autocompleteEl.is(':focus')) {
              evt.preventDefault();
              return false;
            }
          });
          var autocomplete = new google.maps.places.Autocomplete($autocompleteEl.get(0));
          autocomplete.addListener('place_changed', function() {
            var place = autocomplete.getPlace();
            var loc = place.geometry.location;
            var viewport = place.geometry.viewport;
            circle.setLatLng(L.latLng(loc.lat(), loc.lng()));
            circle.addTo(map);
            if (viewport) {
              map.fitBounds([
                viewport.getNorthEast().toJSON(),
                viewport.getSouthWest().toJSON(),
              ]);
            }
            else {
              map.fitBounds(circle.getBounds());
            }
          });
        }


        // save when the editableLayers are edited
        var saveToTextArea = function() {
          var geo = editableLayers.toGeoJSON();
          if (geo.features.length === 0) {
            $el.val("");
            return true
          }
          if (multiple) {
            var coords = $.map(geo.features, function(feature) {
              return [feature.geometry.coordinates];
            })
            geo = {
              "type": geometryType,
              "coordinates": coords
            }
          } else {
            geo = geo.features[0].geometry;
          }
          $el.val(JSON.stringify(geo));
        }

        // handle creation
        map.on('draw:created', function (e) {
          if (!multiple) {
            editableLayers.clearLayers();
          }
          editableLayers.addLayer(e.layer);
          saveToTextArea();
        })
        map.on('draw:edited', saveToTextArea);
        map.on('draw:deleted', saveToTextArea);
      }

      /**
      * Process data-role attribute for the given input element. Feel free to override
      *
      * @param {Selector} $el jQuery selector
      * @param {String} name data-role value
      */
      this.applyStyle = function($el, name) {
        // Process converters first
        for (var conv in fieldConverters) {
            var fieldConv = fieldConverters[conv];

            if (fieldConv($el, name))
                return true;
        }

        // make x-editable's POST compatible with WTForms
        // for x-editable, x-editable-combodate, and x-editable-boolean cases
        var overrideXeditableParams = function(params) {
            var newParams = {};
            newParams['list_form_pk'] = params.pk;
            newParams[params.name] = params.value;
            if ($(this).data('csrf')) {
                newParams['csrf_token'] = $(this).data('csrf');
            }
            return newParams;
        }

        switch (name) {
            case 'select2':
                var opts = {
                    width: 'resolve'
                };

                if ($el.attr('data-allow-blank'))
                    opts['allowClear'] = true;

                if ($el.attr('data-tags')) {
                    $.extend(opts, {
                        tokenSeparators: [','],
                        tags: []
                    });
                }

                $el.select2(opts);
                return true;
            case 'select2-tags':
                // get tags from element
                if ($el.attr('data-tags')) {
                    var tags = JSON.parse($el.attr('data-tags'));
                } else {
                    var tags = [];
                }

                // default to a comma for separating list items
                // allows using spaces as a token separator
                if ($el.attr('data-token-separators')) {
                    var tokenSeparators = JSON.parse($el.attr('data-tags'));
                } else {
                    var tokenSeparators = [','];
                }