// Purpose: To create a map of Kenya using D3.js

function draw_map(country) {

  const id = "#" + country.c.id;
  const svg_map = d3.select(id),
        map_width = +svg_map.attr("width"),
        map_height = +svg_map.attr("height");

  const lat = country.c.latitude;
  const lon = country.c.longitude;

  // Map and projection
  const projection = d3.geoMercator()
      .center([lon+5, lat])                // GPS of location to zoom on
      .scale(400)                       // This is like the zoom
      .translate([ map_width/2, map_height/2 ])

  // Load external data and boot
  d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then( function(data){

      // Filter data
      data.features = data.features.filter(d => {console.log(d.properties.name); return d.properties.name==country.c.name})

      // Draw the map
      svg_map.append("g")
          .selectAll("path")
          .data(data.features)
          .join("path")
            .attr("fill", "grey")
            .attr("d", d3.geoPath()
                .projection(projection)
            )
          .style("stroke", "none")
  })

}