import {
  Button,
  Col,
  Container,
  Modal,
  Row,
  Spacer,
  Text,
} from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { photoTestData } from "../../../consts/photoTestData";
import { useEffect, useState } from "react";
import { getRGB, getRGBFrequency } from "../../../utils/getRGB";
import { plotDensity } from "../../../utils/plotRGB";
import { createPlot } from "../../../utils/createPlot";

const PhotoTestDatasetPage: NextPage = () => {
  const [visible, setVisible] = useState(false);

  const handler = () => {
    setVisible(true);
  };

  const closeHandler = () => {
    setVisible(false);
  };

  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row>
          <Col>
            <Text h3>
              Photo Test Data Set ({photoTestData.files.length} images)
            </Text>
          </Col>
          <Spacer x={2} />
          <Col span={1.5}>
            <Button onClick={handler} auto>
              Plot RGB
            </Button>
          </Col>
        </Row>
        <Modal
          closeButton
          aria-labelledby="modal-title"
          open={visible}
          onClose={closeHandler}
          width="700px"
        >
          <Modal.Body>
            <PlotContainer id="my_dataviz"></PlotContainer>
          </Modal.Body>
          <Modal.Footer>
            <Button auto flat color="error" onPress={closeHandler}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
        <DatasetGrid
          dir="assets/datasets/photo/test"
          filenames={photoTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

const deepMergeSum = (obj1, obj2) => {
  return Object.keys(obj1).reduce((acc, key) => {
    if (typeof obj2[key] === "object") {
      acc[key] = deepMergeSum(obj1[key], obj2[key]);
    } else if (obj2.hasOwnProperty(key) && !isNaN(parseFloat(obj2[key]))) {
      acc[key] = obj1[key] + obj2[key];
    }
    return acc;
  }, {});
};

const PlotContainer = ({ id }) => {
  const calcAndGraph = (imgs: HTMLImageElement[]) => {
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

    const rgbList = imgs.map((img) => {
      return getRGB(img);
    });

    const { rD, gD, bD } = rgbList.reduce(
      (acc, obj) => (acc = deepMergeSum(acc, obj))
    );

    const rData = getRGBFrequency(rD);
    const gData = getRGBFrequency(gD);
    const bData = getRGBFrequency(bD);
    const rDataArray = rData.map<[number, number]>((d) => [d.idx, d.freq]);
    const gDataArray = gData.map<[number, number]>((d) => [d.idx, d.freq]);
    const bDataArray = bData.map<[number, number]>((d) => [d.idx, d.freq]);
    const rFreq = rData.map<number>((d) => d.freq);
    const gFreq = gData.map<number>((d) => d.freq);
    const bFreq = bData.map<number>((d) => d.freq);

    const totalFreq = rFreq.concat(gFreq).concat(bFreq);
    const maxFreq = Math.max(...totalFreq);

    plotDensity(width, height, svg, rDataArray, "red", maxFreq);
    plotDensity(width, height, svg, gDataArray, "green", maxFreq);
    plotDensity(width, height, svg, bDataArray, "blue", maxFreq);
  };

  useEffect(() => {
    const images = photoTestData.files.map((file) => {
      const img = new Image();
      img.src = `/assets/datasets/photo/test/${file}`;
      return img;
    });

    calcAndGraph(images);
  });

  return <Container id={id}></Container>;
};

export default PhotoTestDatasetPage;
