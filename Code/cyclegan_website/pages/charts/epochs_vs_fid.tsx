import { Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { schemeSet1 } from "d3";
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

    const monetPlotContainer = document.getElementById("monet_fid_dataviz");
    if (monetPlotContainer) {
      monetPlotContainer.innerHTML = "";
    }

    const ukiyoePlotContainer = document.getElementById("ukiyoe_fid_dataviz");
    if (ukiyoePlotContainer) {
      ukiyoePlotContainer.innerHTML = "";
    }

    const svgMonet = createPlot(
      "#monet_fid_dataviz",
      width,
      height,
      margin,
      "Epochs vs. FID for Monet",
      "Epochs",
      "FID"
    );

    const svgUkiyoe = createPlot(
      "#ukiyoe_fid_dataviz",
      width,
      height,
      margin,
      "Epochs vs. FID for Ukiyoe",
      "Epochs",
      "FID"
    );

    const monetFIDList = epochFidData.monet.map((d) => d[1]);
    const ukiyoeFIDList = epochFidData.ukiyoe.map((d) => d[1]);

    const monetMinFID = Math.min(...monetFIDList);
    const monetMaxFID = Math.max(...monetFIDList);

    const ukiyoeMinFID = Math.min(...ukiyoeFIDList);
    const ukiyoeMaxFID = Math.max(...ukiyoeFIDList);

    const colorDomain = ["monet", "ukiyoe", "cezanne", "vangogh"];

    // Monet FID plot
    scatterPlot(
      width,
      height,
      svgMonet,
      epochFidData.monet,
      "monet",
      colorDomain,
      schemeSet1,
      [0, 140],
      [monetMinFID - 1, monetMaxFID + 1]
    );

    // Ukiyoe FID plot
    scatterPlot(
      width,
      height,
      svgUkiyoe,
      epochFidData.ukiyoe,
      "ukiyoe",
      colorDomain,
      schemeSet1,
      [0, 140],
      [ukiyoeMinFID - 1, ukiyoeMaxFID + 1]
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
              <Container id="monet_fid_dataviz"></Container>
            </Col>
          </Row>
          <Row>
            <Col css={{ textAlign: "center" }}>
              <Container id="ukiyoe_fid_dataviz"></Container>
            </Col>
          </Row>
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default EpochsVsFidPage;
