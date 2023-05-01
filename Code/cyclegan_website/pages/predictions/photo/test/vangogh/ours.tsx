import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../consts/photoTestData";
import { useState } from "react";
import PlotContainerModal from "../../../../../components/PlotContainerModal";

const PhotoTestToVangoghOursGeneralDatasetPage: NextPage = () => {
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
        <title>Our Test Photo to Van Gogh Predictions</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Col>
              <Text h3>
                Our Test Photo to Van Gogh Predictions (
                {photoTestData.files.length} images)
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
            dir="/assets/predictions/photo/test/vangogh/ours"
          />
          <DatasetGrid
            dir="assets/predictions/photo/test/vangogh/ours"
            filenames={photoTestData.files}
          />
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default PhotoTestToVangoghOursGeneralDatasetPage;
