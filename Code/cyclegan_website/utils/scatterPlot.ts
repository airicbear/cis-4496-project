import {
  Selection,
  ValueFn,
  axisBottom,
  axisLeft,
  line,
  scaleLinear,
  scaleOrdinal,
} from "d3";

export const scatterPlot = (
  width: number,
  height: number,
  svg: Selection<SVGGElement, unknown, HTMLElement, any>,
  data: number[][],
  color: string,
  colorDomain: string[],
  colorScheme: readonly string[],
  domain: number[],
  range: number[]
) => {
  // Add the x axis
  const x = scaleLinear().domain(domain).range([0, width]);
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(axisBottom(x).tickSize(-height).ticks(10));

  // Add the y axis
  const y = scaleLinear().range([height, 0]).domain(range);
  svg
    .append("g")
    .call(
      axisLeft(y)
        .tickSize(-width * 1.3)
        .ticks(7)
    )
    .select(".domain")
    .remove();

  // Add grid
  svg.selectAll(".tick line").attr("stroke", "#DBDBDB");

  // Set color scheme
  const myColor = scaleOrdinal().domain(colorDomain).range(colorScheme);

  // Scatter plot
  svg
    .append("g")
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", (d) => x(d[0]))
    .attr("cy", (d) => y(d[1]))
    .attr("r", 7)
    .style("fill", myColor(color) as string)
    .style("stroke", "white");

  // Line plot
  const path = line()
    .x((d) => x(d[0]))
    .y((d) => y(d[1]));

  svg
    .append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("opacity", "1")
    .attr("stroke", myColor(color) as string)
    .attr("stroke-width", 1)
    .attr("stroke-linejoin", "round")
    .attr("d", path as ValueFn<SVGPathElement, number[][], string>);
};
