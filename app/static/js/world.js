const colours = ['#d7191c','#fdae61','#d3d3d3','#abd9e9','#2c7bb6']

const BACKGROUND_COLOUR = colours[2]
const HIGHLIGHT_COLOUR = colours[1]
const PARTNER_COLOUR = colours[0]
const AFFILIATE_COLOUR = colours[4]
const DEMONSTRATOR_COLOUR = colours[3]

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

    // Function to add interactive elements and fill color to filtered countries
    function addCountryInteractions(countryList, fillColor) {
      let filtered = features.filter(function(d, i) { return countryList.indexOf(d.id) >= 0 });
      filtered.on("mouseover", mouseOverHandler)
          .on("mouseout", mouseOutHandler)
          .on("click", clickHandler)
          .attr("fill", fillColor);
    }

    // Add interactions for CCG output available countries
    let flat_countries = d3.map(countries, d => d.c.id);
    addCountryInteractions(flat_countries, HIGHLIGHT_COLOUR);

    // Add interactions for partner countries
    let partner_countries = ['KEN', 'ZMB', 'LAO', 'GHA', 'VNM', 'IND', 'NPL', 'MWI'];
    addCountryInteractions(partner_countries, PARTNER_COLOUR);

    // Add interactions for associated countries
    let associated_countries = ['ZAF', 'CRI', 'SLE'];
    addCountryInteractions(associated_countries, AFFILIATE_COLOUR);

    // Add interactions for associated countries
    let demonstrator_countries = ['CYP'];
    addCountryInteractions(demonstrator_countries, DEMONSTRATOR_COLOUR);


  // Handmade legend
  const legend_x = 400
  const legend_y = 500
  const legendData = [
    { colour: HIGHLIGHT_COLOUR, text: "CCG Outputs available" },
    { colour: PARTNER_COLOUR, text: "CCG Partner country" },
    { colour: AFFILIATE_COLOUR, text: "CCG Affiliate country" },
    { colour: DEMONSTRATOR_COLOUR, text: "CCG Demonstrator country "}
  ];

  legendData.forEach((item, index) => {
    svg.append("circle")
      .attr("cx", legend_x)
      .attr("cy", legend_y + index * 20)
      .attr("r", 6)
      .style("fill", item.colour);

    svg.append("text")
      .attr("x", legend_x + 20)
      .attr("y", legend_y + index * 20)
      .text(item.text)
      .style("font-size", "15px")
      .attr("alignment-baseline", "middle");
  });
  })

