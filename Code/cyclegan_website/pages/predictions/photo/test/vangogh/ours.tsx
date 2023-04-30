import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../consts/photoTestData";

const PhotoTestToVangoghOursGeneralDatasetPage: NextPage = () => {
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
            <Text h3>Our Test Photo to Van Gogh Predictions</Text>
          </Row>
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
