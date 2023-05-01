import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { ukiyoeTestData } from "../../../consts/ukiyoeTestData";
import { useState } from "react";
import PlotContainerModal from "../../../components/PlotContainerModal";

const UkiyoeTestDatasetPage: NextPage = () => {
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
              Ukiyoe Test Data Set ({ukiyoeTestData.files.length} images)
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
          files={ukiyoeTestData.files}
          dir="/assets/datasets/ukiyoe/test"
        />
        <DatasetGrid
          dir="assets/datasets/ukiyoe/test"
          filenames={ukiyoeTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default UkiyoeTestDatasetPage;
