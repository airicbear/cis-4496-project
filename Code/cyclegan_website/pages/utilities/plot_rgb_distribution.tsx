import {
  Col,
  Container,
  FormElement,
  Input,
  Row,
  Spacer,
  Text,
  useTheme,
} from "@nextui-org/react";
import * as d3 from "d3";
import { NextPage } from "next";
import { ChangeEvent, useRef } from "react";
import AppHeader from "../../components/AppHeader";
import ImageInputLabel from "../../components/ImageInputLabel";
import { getRGB } from "../../utils/getRGB";
import { initializeLabel } from "../../utils/initializeLabel";

const PlotRGBDistributionPage: NextPage = () => {
  const labelRef = useRef<HTMLLabelElement>(null);

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

  const plotDensity = (
    width: number,
    height: number,
    svg,
    data: {},
    color: string
  ) => {
    console.log(`Creating density plot for the ${color} channel.`);
    const processedData = Object.keys(data).map(function (key) {
      return { freq: data[key], idx: +key };
    });

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
      processedData.map(function (d) {
        return d.freq;
      })
    );

    console.log(processedData);

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

  const calcAndGraph = (img: HTMLImageElement) => {
    const { rD, gD, bD } = getRGB(img);

    // Set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 50, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    document.getElementById("my_dataviz").innerHTML = "";

    // Append the svg object to the body of the page
    const svg = d3
      .select("#my_dataviz")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg
      .append("text")
      .attr("text-anchor", "end")
      .attr("transform", "rotate(-90)")
      .attr("y", -margin.left + 20)
      .attr("x", -margin.top)
      .text("Density");

    svg
      .append("text")
      .attr("text-anchor", "end")
      .attr("x", width)
      .attr("y", height + margin.top + 20)
      .text("RGB value");

    plotDensity(width, height, svg, rD, "red");
    plotDensity(width, height, svg, gD, "green");
    plotDensity(width, height, svg, bD, "blue");
  };

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const image = new Image();

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const file = files[0];

    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        initializeLabel(labelRef.current, `url(${reader.result})`);
        image.src = reader.result as string;
      },
      false
    );
    image.onload = () => {
      calcAndGraph(image);
    };
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Plot RGB Distribution</Text>
        </Row>
        <Row align="center">
          <Col css={{ textAlign: "center" }}>
            <Text>Input</Text>
          </Col>
        </Row>
        <Row align="center">
          <Col css={{ textAlign: "center" }}>
            <form style={{ textAlign: "center" }}>
              <Input
                type="file"
                id={"input-file-upload"}
                accept=".jpg, .jpeg, .png"
                onChange={handleChange}
                css={{
                  display: "none",
                }}
              ></Input>
              <ImageInputLabel
                htmlFor={"input-file-upload"}
                id={"label-input-rgb-distribution"}
                labelRef={labelRef}
                imageOnLoad={(image) => {
                  calcAndGraph(image);
                }}
              />
            </form>
          </Col>
        </Row>
        <Row>
          <Col css={{ textAlign: "center" }}>
            <Container id="my_dataviz"></Container>
          </Col>
        </Row>
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PlotRGBDistributionPage;
