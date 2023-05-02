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
import { useState } from "react";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { photoTestData } from "../../../consts/photoTestData";
import PlotContainerModal from "../../../components/PlotContainerModal";

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
        <PlotContainerModal
          visible={visible}
          closeHandler={closeHandler}
          files={photoTestData.files}
          dir="/assets/datasets/photo/test"
        />
        <DatasetGrid
          dir="assets/datasets/photo/test"
          filenames={photoTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PhotoTestDatasetPage;
