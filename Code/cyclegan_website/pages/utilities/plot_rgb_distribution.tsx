import {
  Col,
  Container,
  FormElement,
  Input,
  Row,
  Spacer,
  Text,
} from "@nextui-org/react";
import { NextPage } from "next";
import { ChangeEvent, useRef } from "react";
import AppHeader from "../../components/AppHeader";
import ImageInputLabel from "../../components/ImageInputLabel";
import ImageInputTitle from "../../components/ImageInputTitle";
import { createPlot } from "../../utils/createPlot";
import { getRGB, getRGBFrequency } from "../../utils/getRGB";
import { initializeLabel } from "../../utils/initializeLabel";
import { plotDensity } from "../../utils/plotRGB";

const PlotRGBDistributionPage: NextPage = () => {
  const labelRef = useRef<HTMLDivElement>(null);

  const calcAndGraph = (img: HTMLImageElement) => {
    // Set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 50, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

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
      "RGB Distribution",
      "RGB Value",
      "Frequency"
    );

    const { rD, gD, bD } = getRGB(img);
    const rData = getRGBFrequency(rD);
    const gData = getRGBFrequency(gD);
    const bData = getRGBFrequency(bD);
    const rDataArray = rData.map<[number, number]>((d) => [d.idx, d.freq]);
    const gDataArray = gData.map<[number, number]>((d) => [d.idx, d.freq]);
    const bDataArray = bData.map<[number, number]>((d) => [d.idx, d.freq]);
    const rFreq = rData.map<number>((d) => d.freq);
    const gFreq = gData.map<number>((d) => d.freq);
    const bFreq = bData.map<number>((d) => d.freq);

    // Used to scale axis
    const totalFreq = rFreq.concat(gFreq).concat(bFreq);
    const maxFreq = Math.max(...totalFreq);

    plotDensity(width, height, svg, rDataArray, "red", maxFreq);
    plotDensity(width, height, svg, gDataArray, "green", maxFreq);
    plotDensity(width, height, svg, bDataArray, "blue", maxFreq);
  };

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const image = new Image();

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const file = files ? files[0] : null;

    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        if (labelRef.current) {
          initializeLabel(labelRef.current, `url(${reader.result})`);
        }
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
            <ImageInputTitle />
          </Col>
        </Row>
        <Row align="center">
          <Col css={{ textAlign: "center" }}>
            <form style={{ textAlign: "center" }}>
              <Input
                type="file"
                id={"input-file-upload"}
                accept="image/*"
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
        <Spacer y={2} />
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
