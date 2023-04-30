import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { monetTestData } from "../../../../../consts/monetTestData";
import Head from "next/head";

const MonetTestToPhotoAuthorsDatasetPage: NextPage = () => {
  return (
    <>
      <Head>
        <title>Test Monet to Photo Predictions (Author's)</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Text h3>Test Monet to Photo Predictions (Author's)</Text>
          </Row>
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
