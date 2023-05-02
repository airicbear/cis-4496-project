import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { photoTrainData } from "../../../consts/photoTrainData";
import { useState } from "react";
import PlotContainerModal from "../../../components/PlotContainerModal";

const PhotoTrainDatasetPage: NextPage = () => {
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
        <Row align="center">
          <Col>
            <Text h3>
              Photo Train Data Set ({photoTrainData.files.length} images)
            </Text>
          </Col>
          <Spacer x={2} />
          <Col span={1.5}>
            <Button onClick={handler} auto>
              Plot RGB
            </Button>
          </Col>
        </Row>
        <PlotContainerModal
          visible={visible}
          closeHandler={closeHandler}
          files={photoTrainData.files}
          dir="/assets/datasets/photo/train"
        />
        <DatasetGrid
          dir="assets/datasets/photo/train"
          filenames={photoTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PhotoTrainDatasetPage;
