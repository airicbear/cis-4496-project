import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../../../components/AppHeader";
import DatasetGrid from "../../../../../../components/DatasetGrid";
import { monetTestData } from "../../../../../../consts/monetTestData";
import Head from "next/head";
import PlotContainerModal from "../../../../../../components/PlotContainerModal";
import { useState } from "react";

const MonetTestToPhotoOursGeneralDatasetPage: NextPage = () => {
  const [visible, setVisible] = useState(false);

  const handler = () => {
    setVisible(true);
  };

  const closeHandler = () => {
    setVisible(false);
  };

  return (
    <>
      <Head>
        <title>Our Test Monet to Photo Predictions (General)</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Col>
              <Text h3>
                Our Test Monet to Photo Predictions (General) (
                {monetTestData.files.length} images)
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
            files={monetTestData.files}
            dir="/assets/predictions/monet/test/photo/ours/general"
          />
          <DatasetGrid
            dir="assets/predictions/monet/test/photo/ours/general"
            filenames={monetTestData.files}
          />
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default MonetTestToPhotoOursGeneralDatasetPage;
