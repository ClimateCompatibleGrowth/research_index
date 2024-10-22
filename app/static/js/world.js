const colours = ['#d7191c','#fdae61','#ffffbf','#abd9e9','#2c7bb6']

const BACKGROUND_COLOUR = colours[3]
const HIGHLIGHT_COLOUR = colours[1]
const PARTNER_COLOUR = colours[0]
const ASSOC_COLOUR = colours[4]
const HOVER_COLOUR = colours[2]

function mouseOverHandler(d, i) {
    d3.select(this).transition().duration('50').attr('opacity', '.85');
  }
  function mouseOutHandler(d, i) {
    d3.select(this).transition().duration('50').attr('opacity', '1')
  }
  function clickHandler(d, i) {
    const url = "/countries/" + i.id
    window.location.assign(url, '_blank')
  }


// The svg
const svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

// svg.append("rect")
//     .attr("width", width)
//     .attr("height", height)
//     .attr("fill", colours[2]);

// Map and projection
const projection = d3.geoNaturalEarth1()
    .scale(width / 1.1 / Math.PI)
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

    // Add different actions for partner countries
    let partner_countries = ['KEN', 'ZMB', 'LAO', 'GHA', 'VNM', 'IND', 'NPL', 'MWI']
    filtered = features.filter(function(d,i){ return partner_countries.indexOf(d.id) >= 0 })

    // Add the interactive elements for the filtered countries
    filtered.on("mouseover", mouseOverHandler)
    .on("mouseout", mouseOutHandler)
    .on("click", clickHandler)
    .attr("fill", PARTNER_COLOUR);

    // Add different actions for associated countries
    let associated_countries = ['ZAF', 'CRI', 'SLE']
    filtered = features.filter(function(d,i){ return associated_countries.indexOf(d.id) >= 0 })

    // Add the interactive elements for the filtered countries
    filtered.on("mouseover", mouseOverHandler)
    .on("mouseout", mouseOutHandler)
    .on("click", clickHandler)
    .attr("fill", ASSOC_COLOUR);


  // Handmade legend
  const legend_x = 400
  const legend_y = 500
  svg.append("circle").attr("cx",legend_x).attr("cy",legend_y).attr("r", 6).style("fill", HIGHLIGHT_COLOUR)
  svg.append("circle").attr("cx",legend_x).attr("cy",legend_y + 20).attr("r", 6).style("fill", PARTNER_COLOUR)
  svg.append("circle").attr("cx",legend_x).attr("cy",legend_y + 40).attr("r", 6).style("fill", ASSOC_COLOUR)

  svg.append("text").attr("x", legend_x + 20).attr("y", legend_y).text("CCG outputs available").style("font-size", "15px").attr("alignment-baseline","middle")
  svg.append("text").attr("x", legend_x + 20).attr("y", legend_y + 20).text("CCG partner country").style("font-size", "15px").attr("alignment-baseline","middle")
  svg.append("text").attr("x", legend_x + 20).attr("y", legend_y + 40).text("CCG associated country").style("font-size", "15px").attr("alignment-baseline","middle")
  })

