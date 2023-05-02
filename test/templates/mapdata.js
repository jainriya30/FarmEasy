let all_states = {{ states }};

function fix_missing_state(state_name) {
  if (state_name == "Telangana") return "Andhra Pradesh";
  if (state_name == "Ladakh") return "Jammu and Kashmir";
  return state_name;
}

function highlight_states(states) {

  _clear_existing_highlight();
  simplemaps_countrymap.refresh();

  if (states.length == 0) return;

  states = JSON.parse(states);  
  for(var i in states) {
    var state_name = states[i];
    state_name = fix_missing_state(state_name);
    var state_index = all_states.indexOf(state_name);

    var state_data = simplemaps_countrymap_mapdata.state_specific[state_index];
    state_data.color = 'yellow';
  }  
  simplemaps_countrymap.refresh();
}

function _clear_existing_highlight() {
  for(var i in simplemaps_countrymap_mapdata.state_specific) {
    var state_data = simplemaps_countrymap_mapdata.state_specific[i];
    state_data.color = 'green';
  }
}

function clear_existing_highlight() {
  _clear_existing_highlight();
  simplemaps_countrymap.refresh();
}

var simplemaps_countrymap_mapdata={
    main_settings: {
      /* General settings */
      width: "responsive",
      background_color: "#ffffff",
      background_transparent: "yes",
      border_color: "black",
      state_description: `Unavailable`,
      state_color: "green",
      state_hover_color: "yellow",
      state_url: "#",
      border_size: "2",
      all_states_inactive: "no",
      all_states_zoomable: "no",
      
      /* Location defaults */
      location_description: "Location description",
      location_color: "#FF0067",
      location_opacity: 0.8,
      location_hover_opacity: 1,
      location_url: "",
      location_size: 25,
      location_type: "square",
      location_image_source: "frog.png",
      location_border_color: "#FFFFFF",
      location_border: 2,
      location_hover_border: 2.5,
      all_locations_inactive: "no",
      all_locations_hidden: "no",
      
      /* Label defaults */
      label_color: "#d5ddec",
      label_hover_color: "#d5ddec",
      label_size: 22,
      label_font: "Arial",
      hide_labels: "no",
      hide_eastern_labels: "no",
     
      /* Zoom settings */
      zoom: "yes",
      back_image: "no",
      initial_back: "no",
      initial_zoom: "-1",
      initial_zoom_solo: "no",
      region_opacity: 1,
      region_hover_opacity: 0.6,
      zoom_out_incrementally: "yes",
      zoom_percentage: 0.99,
      zoom_time: 0.5,
      
      /* Popup settings */
      popup_color: "white",
      popup_opacity: 0.9,
      popup_shadow: 1,
      popup_corners: 5,
      popup_font: "12px/1.5 Verdana, Arial, Helvetica, sans-serif",
      popup_nocss: "no",
      
      /* Advanced settings */
      div: "map",
      auto_load: "yes",
      url_new_tab: "no",
      images_directory: "default",
      fade_time: 0.1,
      link_text: "View Website",
      popups: "detect",
      state_image_url: "",
      state_image_position: "",
      location_image_url: ""
    },
    
    state_specific: {
    {% for i in range(states|length) %}
        {% if states[i] %}
            "{{ i }}" : {
                name: "{{ states[i] }}",
                color: "green",
                {% if states[i] in crop_data %}description: `<ol>{% for crop in crop_data[states[i]] %}<li>{{ crop.title() }}</li>{% endfor %}</ol>`{% endif %}
            },
        {% endif%}      
    {% endfor %}    
    },
    locations: {},
    labels: {},
    legend: {
      entries: []
    },
    regions: {}
  };