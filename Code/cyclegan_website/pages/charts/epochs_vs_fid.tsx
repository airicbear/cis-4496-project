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
  const makeScatterPlot = (
    id: string,
    width: number,
    height: number,
    margin: {
      top: number;
      right: number;
      bottom: number;
      left: number;
    },
    data: number[][],
    title: string,
    color: string
  ) => {
    const plotContainer = document.getElementById(id);
    if (plotContainer) {
      plotContainer.innerHTML = "";
    }

    const svg = createPlot(
      `#${id}`,
      width,
      height,
      margin,
      title,
      "Epochs",
      "FID"
    );

    const fidList = data.map((d) => d[1]);

    const minFID = Math.min(...fidList);
    const maxFID = Math.max(...fidList);

    const colorDomain = ["monet", "ukiyoe", "cezanne", "vangogh"];

    scatterPlot(
      width,
      height,
      svg,
      data,
      color,
      colorDomain,
      schemeSet1,
      [0, 140],
      [minFID - 1, maxFID + 1]
    );
  };

  useEffect(() => {
    // Set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 60, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 405 - margin.top - margin.bottom;

    makeScatterPlot(
      "monet_fid_dataviz",
      width,
      height,
      margin,
      epochFidData.monet,
      "Epochs vs. FID for Monet",
      "monet"
    );

    makeScatterPlot(
      "ukiyoe_fid_dataviz",
      width,
      height,
      margin,
      epochFidData.ukiyoe,
      "Epochs vs. FID for Ukiyo-e",
      "ukiyoe"
    );

    makeScatterPlot(
      "cezanne_fid_dataviz",
      width,
      height,
      margin,
      epochFidData.cezanne,
      "Epochs vs. FID for Cezanne",
      "cezanne"
    );

    makeScatterPlot(
      "vangogh_fid_dataviz",
      width,
      height,
      margin,
      epochFidData.vangogh,
      "Epochs vs. FID for Van Gogh",
      "vangogh"
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
          <Row>
            <Col css={{ textAlign: "center" }}>
              <Container id="cezanne_fid_dataviz"></Container>
            </Col>
          </Row>
          <Row>
            <Col css={{ textAlign: "center" }}>
              <Container id="vangogh_fid_dataviz"></Container>
            </Col>
          </Row>
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default EpochsVsFidPage;
