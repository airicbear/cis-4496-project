import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { monetTestData } from "../../../../../consts/monetTestData";
import Head from "next/head";
import { useState } from "react";
import PlotContainerModal from "../../../../../components/PlotContainerModal";

const MonetTestToPhotoAuthorsDatasetPage: NextPage = () => {
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
        <title>Author's Test Monet to Photo Predictions</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Col>
              <Text h3>
                Author's Test Monet to Photo Predictions (
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
            files={monetTestData.files.map((filename) =>
              filename.replace("jpg", "png")
            )}
            dir="/assets/predictions/monet/test/photo/authors"
          />
          <DatasetGrid
            dir="assets/predictions/monet/test/photo/authors"
            filenames={monetTestData.files.map((filename) =>
              filename.replace("jpg", "png")
            )}
          />
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default MonetTestToPhotoAuthorsDatasetPage;
