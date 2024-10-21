const HOVER_COLOUR = "#f03b20"
const HIGHLIGHT_COLOUR = "#feb24c"
const BACKGROUND_COLOUR = "#ffeda0"

function mouseOverHandler(d, i) {
    d3.select(this).attr("fill", HOVER_COLOUR)
  }
  function mouseOutHandler(d, i) {
    d3.select(this).attr("fill", HIGHLIGHT_COLOUR)
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

     // create initial features selection based on data
     let features = d3.select("svg").selectAll("path").data(data.features);

     // add new features to the selection using the enter selection,
     // and merge back into the original update selection
     features = features.enter().append("path")
         .attr("fill", BACKGROUND_COLOUR)
         .attr("d", d3.geoPath()
         .projection(projection)
         )
         .style("stroke", "#fff")
         .merge(features);

    // Get a list of country ids
    let flat_countries = d3.map(countries, d => d.c.id)

    // Filter the existing features that match the countries
    let filtered = features.filter(function(d,i){ return flat_countries.indexOf(d.id) >= 0 })

    // Add the interactive elements for the filtered countries
    filtered.on("mouseover", mouseOverHandler)
              .on("mouseout", mouseOutHandler)
              .on("click", clickHandler)
              .attr("fill", HIGHLIGHT_COLOUR);

  })

