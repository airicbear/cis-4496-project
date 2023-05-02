import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { vangoghTestTrainData } from "../../../consts/vangoghTestTrainData";
import { useState } from "react";
import PlotContainerModal from "../../../components/PlotContainerModal";

const VangoghTestDatasetPage: NextPage = () => {
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
              Vangogh Test/Train Data Set ({vangoghTestTrainData.files.length}{" "}
              images)
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
          files={vangoghTestTrainData.files}
          dir="/assets/datasets/vangogh/test-train"
        />
        <DatasetGrid
          dir="assets/datasets/vangogh/test-train"
          filenames={vangoghTestTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default VangoghTestDatasetPage;
