// static/js/network.js

function main() {

// Specify the dimensions of the chart.
const width = 928;
const height = 680;

// Specify the color scale.
const color = d3.scaleOrdinal(d3.schemeCategory10);

// The force simulation mutates links and nodes, so create a copy
// so that re-evaluating this cell produces the same result.
const links = data_links;
const nodes = data_nodes;

// Create a tooltip div that is hidden by default.
var div = d3.select("body").append("div")
   .attr("class", "tooltip-node")
   .style("opacity", 0);

// Create a simulation with several forces.
const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id))
    .force("charge", d3.forceManyBody())
    .force("x", d3.forceX())
    .force("y", d3.forceY());

// Create the SVG container.
const svg = d3.select("#network")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [-width / 2, -height / 2, width, height])
    .attr("style", "max-width: 100%; height: auto;");

// Add a line for each link, and a circle for each node.
const link = svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(links)
  .join("line")
    .attr("stroke-width", d => 2);

const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
  .selectAll("circle")
  .data(nodes)
  .join("circle")
    .attr("r", 5)
    .attr("fill", d => color(d.group));

node.append("title")
    .text(d => d.name);

node.on("dblclick", dblclick)

node.on("mouseover", function(event, d) {

  div.transition()
    .duration(200)
    .style("opacity", .9);

  div.html(d.name)
   .style("left", (event.pageX + 10) + "px")
   .style("top", (event.pageY - 15) + "px");

  })

// Add a drag behavior.
node.call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

function dblclick(event, a){
  const url = ""
 switch(a.group) {
  case 0:
      url = "/authors/" + a.id
      break;
  case 1:
      url = "/outputs/" + a.id
      break;
 }
 window.location.assign(url, '_blank');
}

// Set the position attributes of links and nodes each time the simulation ticks.
simulation.on("tick", () => {
  link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

  node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
});

// Reheat the simulation when drag starts, and fix the subject position.
function dragstarted(event) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  event.subject.fx = event.subject.x;
  event.subject.fy = event.subject.y;
}

// Update the subject (dragged node) position during drag.
function dragged(event) {
  event.subject.fx = event.x;
  event.subject.fy = event.y;
}

// Restore the target alpha so the simulation cools after dragging ends.
// Unfix the subject position now that it’s no longer being dragged.
function dragended(event) {
  if (!event.active) simulation.alphaTarget(0);
  event.subject.fx = null;
  event.subject.fy = null;
}

// When this cell is re-run, stop the previous simulation. (This doesn’t
// really matter since the target alpha is zero and the simulation will
// stop naturally, but it’s a good practice.)
//   invalidation.then(() => simulation.stop());
}
main();