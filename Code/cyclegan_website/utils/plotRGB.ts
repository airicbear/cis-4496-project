import * as d3 from "d3";

export const plotDensity = (
  width: number,
  height: number,
  svg: d3.Selection<SVGGElement, unknown, HTMLElement, any>,
  data: number[][],
  color: string,
  maxFreq: number
) => {
  console.log(`Creating density plot for the ${color} channel.`);

  // Add the x axis
  const x = d3.scaleLinear().domain([0, 255]).range([0, width]);
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // Add the y axis
  const y = d3.scaleLinear().range([height, 0]).domain([0, maxFreq]);
  svg.append("g").call(d3.axisLeft(y));

  const area = d3
    .area()
    .curve(d3.curveBasis)
    .x((d) => x(d[0]))
    .y1((d) => y(d[1]))
    .y0(height);

  svg
    .append("path")
    .datum(data)
    .attr("fill", color)
    .attr("opacity", ".5")
    .attr("d", area as any);

  const path = d3
    .line()
    .curve(d3.curveBasis)
    .x((d) => x(d[0]))
    .y((d) => y(d[1]));

  svg
    .append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("opacity", "1")
    .attr("stroke", color)
    .attr("stroke-width", 1)
    .attr("stroke-linejoin", "round")
    .attr("d", path as any);
};
