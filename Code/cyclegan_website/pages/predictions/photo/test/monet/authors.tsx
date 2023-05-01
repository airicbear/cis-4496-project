import { Button, Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../consts/photoTestData";
import PlotContainerModal from "../../../../../components/PlotContainerModal";
import { useState } from "react";

const PhotoTestToMonetAuthorsDatasetPage: NextPage = () => {
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
        <title>Author's Test Photo to Monet Predictions</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Col>
              <Text h3>
                Author's Test Photo to Monet Predictions (
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
            files={photoTestData.files.map((filename) =>
              filename.replace("jpg", "png")
            )}
            dir="/assets/predictions/photo/test/monet/authors"
          />
          <DatasetGrid
            dir="assets/predictions/photo/test/monet/authors"
            filenames={photoTestData.files.map((filename) =>
              filename.replace("jpg", "png")
            )}
          />
          <Spacer y={2} />
        </Container>
      </Container>
    </>
  );
};

export default PhotoTestToMonetAuthorsDatasetPage;
