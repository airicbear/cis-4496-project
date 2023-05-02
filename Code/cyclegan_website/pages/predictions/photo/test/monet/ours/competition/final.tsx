import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../../../../components/AppHeader";
import DatasetGrid from "../../../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../../../consts/photoTestData";
import Head from "next/head";
import PlotContainerModal from "../../../../../../../components/PlotContainerModal";
import { useState } from "react";

const PhotoTestToMonetOursCompetitionFinalDatasetPage: NextPage = () => {
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
        <title>Our Test Photo to Monet Predictions (Competition, Final)</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Col>
              <Text h3>
                Our Test Photo to Monet Predictions (Competition, Final) (
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
            dir="/assets/predictions/photo/test/monet/ours/competition/final"
          />
          <DatasetGrid
            dir="assets/predictions/photo/test/monet/ours/competition/final"
            filenames={photoTestData.files}
          />
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default PhotoTestToMonetOursCompetitionFinalDatasetPage;
