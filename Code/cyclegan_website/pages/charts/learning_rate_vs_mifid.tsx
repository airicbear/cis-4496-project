import { Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import {
  ValueFn,
  axisBottom,
  axisLeft,
  line,
  scaleLinear,
  scaleOrdinal,
  schemeSet1,
} from "d3";
import { NextPage } from "next";
import Head from "next/head";
import { useEffect } from "react";
import AppHeader from "../../components/AppHeader";
import { learningRateMiFidData } from "../../consts/learningRateMiFidData";
import { createPlot } from "../../utils/createPlot";

const EpochsVsMiFidPage: NextPage = () => {
  useEffect(() => {
    // Set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 60, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 405 - margin.top - margin.bottom;

    const plotContainer = document.getElementById("my_dataviz");
    if (plotContainer) {
      plotContainer.innerHTML = "";
    }

    const svg = createPlot(
      "#my_dataviz",
      width,
      height,
      margin,
      "Learning Rate vs. MiFID",
      "Learning Rate",
      "MiFID"
    );

    const miFidList = learningRateMiFidData.epochs30.map((d) => d[1]);

    const minFID = Math.min(...miFidList);
    const maxFID = Math.max(...miFidList);

    const colorDomain = ["demo1", "demo2", "demo3"];

    // Add the x axis
    const x = scaleLinear().domain([0, 0.0001]).range([0, width]);
    svg
      .append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(axisBottom(x).tickSize(-height).ticks(10));

    // Add the y axis
    const y = scaleLinear()
      .range([height, 0])
      .domain([minFID - 0.2, maxFID + 0.2]);
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
    const myColor = scaleOrdinal().domain(colorDomain).range(schemeSet1);

    // Scatter plot
    svg
      .append("g")
      .selectAll("dot")
      .data(learningRateMiFidData.epochs30)
      .enter()
      .append("circle")
      .attr("cx", (d) => x(d[0]))
      .attr("cy", (d) => y(d[1]))
      .attr("r", 7)
      .style("fill", myColor("demo1") as string)
      .style("stroke", "white");

    // Line plot
    const path = line()
      .x((d) => x(d[0]))
      .y((d) => y(d[1]));

    svg
      .append("path")
      .datum(learningRateMiFidData.epochs30)
      .attr("fill", "none")
      .attr("opacity", "1")
      .attr("stroke", myColor("demo1") as string)
      .attr("stroke-width", 1)
      .attr("stroke-linejoin", "round")
      .attr("d", path as ValueFn<SVGPathElement, number[][], string>);
  });

  return (
    <>
      <Head>
        <title>Learning Rate vs. MiFID</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Text h3>Learning Rate vs. MiFID</Text>
          </Row>
          <Row>
            <Col css={{ textAlign: "center" }}>
              <Container id="my_dataviz"></Container>
            </Col>
          </Row>
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default EpochsVsMiFidPage;
