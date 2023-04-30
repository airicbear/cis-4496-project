import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../consts/photoTestData";

const PhotoTestToMonetAuthorsDatasetPage: NextPage = () => {
  return (
    <>
      <Head>
        <title>Test Photo to Monet Predictions (Author's)</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Text h3>Test Photo to Monet Predictions (Author's)</Text>
          </Row>
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
