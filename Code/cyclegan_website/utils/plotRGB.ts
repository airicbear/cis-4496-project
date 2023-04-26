import {
  Selection,
  ValueFn,
  area,
  axisBottom,
  axisLeft,
  curveBasis,
  line,
  scaleLinear,
} from "d3";

export const plotDensity = (
  width: number,
  height: number,
  svg: Selection<SVGGElement, unknown, HTMLElement, any>,
  data: number[][],
  color: string,
  maxFreq: number
) => {
  console.log(`Creating density plot for the ${color} channel.`);

  // Add the x axis
  const x = scaleLinear().domain([0, 255]).range([0, width]);
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(axisBottom(x));

  // Add the y axis
  const y = scaleLinear().range([height, 0]).domain([0, maxFreq]);
  svg.append("g").call(axisLeft(y));

  const areaUnderCurve = area()
    .curve(curveBasis)
    .x((d) => x(d[0]))
    .y1((d) => y(d[1]))
    .y0(height);

  svg
    .append("path")
    .datum(data)
    .attr("fill", color)
    .attr("opacity", ".5")
    .attr("d", areaUnderCurve as ValueFn<SVGPathElement, number[][], string>);

  const path = line()
    .curve(curveBasis)
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
    .attr("d", path as ValueFn<SVGPathElement, number[][], string>);
};
