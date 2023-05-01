import { Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { schemeSet1, schemeSet2 } from "d3";
import { NextPage } from "next";
import Head from "next/head";
import { useEffect } from "react";
import AppHeader from "../../components/AppHeader";
import { epochFidData } from "../../consts/epochFidData";
import { createPlot } from "../../utils/createPlot";
import { scatterPlot } from "../../utils/scatterPlot";

const EpochsVsFidPage: NextPage = () => {
  useEffect(() => {
    // Set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 60, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 405 - margin.top - margin.bottom;

    const plotContainer = document.getElementById("my_dataviz");
    if (plotContainer) {
      plotContainer.innerHTML = "";
    }

    // Append the svg object to the body of the page
    const svg = createPlot(
      "#my_dataviz",
      width,
      height,
      margin,
      "Epochs vs. FID for Monet",
      "Epochs",
      "FID"
    );

    const totalFreq = epochFidData.monet.map((d) => d[1]);
    const maxFreq = Math.max(...totalFreq);
    const colorDomain = ["monet", "ukiyoe", "cezanne", "vangogh"];

    scatterPlot(
      width,
      height,
      svg,
      epochFidData.monet,
      "monet",
      colorDomain,
      schemeSet1,
      [0, 140],
      [102, maxFreq + 1]
    );
  });

  return (
    <>
      <Head>
        <title>Epochs vs. FID</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Text h3>Epochs vs. FID</Text>
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

export default EpochsVsFidPage;
