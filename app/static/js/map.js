const colours = ['#d7191c','#fdae61','#d3d3d3','#abd9e9','#2c7bb6']

const BACKGROUND_COLOUR = colours[2]
const HIGHLIGHT_COLOUR = colours[1]
const PARTNER_COLOUR = colours[0]
const AFFILIATE_COLOUR = colours[4]
const DEMONSTRATOR_COLOUR = colours[3]


// Purpose: To create a map of Kenya using D3.js

function draw_map(country) {

  // This should be replaced with information drawn from the backend database (ccg_status tag)
  let partner_countries = ['KEN', 'ZMB', 'LAO', 'GHA', 'VNM', 'IND', 'NPL', 'MWI'];
  let affiliated_countries = ['ZAF', 'CRI', 'SLE'];
  let demonstrator_countries = ['CYP'];

  var fill

  if (partner_countries.indexOf(country.c.id) >= 0) {
    fill = PARTNER_COLOUR
  } else if (affiliated_countries.indexOf(country.c.id) >= 0) {
    fill = AFFILIATE_COLOUR
  } else if ((demonstrator_countries.indexOf(country.c.id) >= 0)) {
    fill = DEMONSTRATOR_COLOUR
  } else {
    fill = HIGHLIGHT_COLOUR
  }
  // Above should be replaced with information drawn from the backend database

  const id = "#" + country.c.id;
  const svg_map = d3.select(id),
        map_width = +svg_map.attr("width"),
        map_height = +svg_map.attr("height");

  const lat = country.c.latitude;
  const lon = country.c.longitude;

  // Load external data and boot
  d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then( function(data){

      // Filter data
      country = data.features.filter(d => {console.log(d.properties.name); return d.properties.name==country.c.name})

    // Initial Map and projection
    const initial_projection = d3.geoMercator()
    .center([lon, lat])                // GPS of location to zoom on
    .scale(400)                       // This is like the zoom
    .translate([ map_width/2, map_height/2 ])

    var box = d3.geoBounds(country[0])
    var box_width = box[1][0] - box[0][0]
    var box_height = box[1][1] - box[0][1]
    var centroid = [box[0][0] + box_width / 2, box[0][1] + box_height / 2];
    var zoomScaleFactor = map_height / box_height;
    var zoomX = centroid[0];
    var zoomY = centroid[1];

    if (box.width > box.height) {
      zoomScaleFactor = baseHeight / box_width;
  }

    // Map and projection
    const scaled_projection = d3.geoMercator()
    .center(centroid)                // GPS of location to zoom on
    .scale(zoomScaleFactor * 40)     // This is like the zoom
    .translate([ map_width / 2, map_height / 2 ])

      // Draw the map
      svg_map.append("g")
          .selectAll("path")
          .data(country)
          .join("path")
            .attr("fill", fill)
            .attr("d", d3.geoPath()
                .projection(scaled_projection)
            )
          .style("stroke", "none")
  })

}