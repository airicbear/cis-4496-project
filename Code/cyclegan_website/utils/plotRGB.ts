import * as d3 from "d3";

// Function to compute density
function kernelDensityEstimator(kernel, X) {
  return function (V) {
    return X.map(function (x) {
      return [
        x,
        d3.mean(V, function (v) {
          return kernel(x - (v as number));
        }),
      ];
    });
  };
}

function kernelEpanechnikov(k) {
  return function (v) {
    return Math.abs((v /= k)) <= 1 ? (0.75 * (1 - v * v)) / k : 0;
  };
}

export const plotDensity = (
  width: number,
  height: number,
  svg,
  data: {
    freq: number;
    idx: number;
  }[],
  color: string
) => {
  console.log(`Creating density plot for the ${color} channel.`);

  // Add the x axis
  const x = d3.scaleLinear().domain([0, 255]).range([0, width]);
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

  // Add the y axis
  const y = d3.scaleLinear().range([height, 0]).domain([0, 0.01]);
  svg.append("g").call(d3.axisLeft(y));

  // Compute kernel density estimation
  const kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(40));
  const density = kde(
    data.map(function (d) {
      return d.freq;
    })
  );

  console.log(data);

  // Plot the area
  svg
    .append("path")
    .datum(density)
    .attr("fill", color)
    .attr("opacity", ".5")
    .attr(
      "d",
      d3
        .area()
        .curve(d3.curveBasis)
        .x((d) => x(d[0]))
        .y1((d) => y(d[1]))
        .y0(height)
    );

  svg
    .append("path")
    .datum(density)
    .attr("fill", "none")
    .attr("opacity", "1")
    .attr("stroke", color)
    .attr("stroke-width", 1)
    .attr("stroke-linejoin", "round")
    .attr(
      "d",
      d3
        .line()
        .curve(d3.curveBasis)
        .x((d) => x(d[0]))
        .y((d) => y(d[1]))
    );
};
