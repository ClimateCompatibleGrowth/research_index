const HOVER_COLOR = "#d36f80"


function mouseOverHandler(d, i) {
    d3.select(this).attr("fill", HOVER_COLOR)
  }
  function mouseOutHandler(d, i) {
    d3.select(this).attr("fill", "red")
  }
  function clickHandler(d, i) {
    const url = "/countries/" + i.id
    window.location.assign(url, '_blank')
  }


// The svg
const svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

// Map and projection
const projection = d3.geoNaturalEarth1()
    .scale(width / 1.3 / Math.PI)
    .translate([width / 2, height / 2])


const countries = country_data;

// Load external data and draw base map
d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then( function(data) {

    // Draw the map
    svg.append("g")
        .selectAll("path")
        .data(data.features)
        .join("path")
            .attr("fill", "#69b3a2")
            .attr("d", d3.geoPath()
            .projection(projection)
            )
            .style("stroke", "#fff")
})

  // Load external data and highlight countries
  d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson").then( function(data){

      // Filter data

      countries.forEach(country => {

          const filtered_data = data.features.filter(d => {return d.properties.name==country.c.name})

          // Draw the map
          svg.append("g")
              .selectAll("path")
              .data(filtered_data)
              .join("path")
                .attr("fill", "red")
                .attr("d", d3.geoPath()
                    .projection(projection)
                )
              .style("stroke", "#fff")
              .on("mouseover", mouseOverHandler)
              .on("mouseout", mouseOutHandler)
              .on("click", clickHandler)

      }
      );

  })

