import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../../../components/AppHeader";
import DatasetGrid from "../../../../../../components/DatasetGrid";
import { monetTestData } from "../../../../../../consts/monetTestData";
import Head from "next/head";

const MonetTestToPhotoOursGeneralDatasetPage: NextPage = () => {
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
            <Text h3>Our Test Monet to Photo Predictions (General)</Text>
          </Row>
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
