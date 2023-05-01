import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../consts/photoTestData";

const PhotoTestToUkiyoeAuthorsDatasetPage: NextPage = () => {
  return (
    <>
      <Head>
        <title>Author's Test Photo to Ukiyoe Predictions</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Text h3>
              Author's Test Photo to Ukiyoe Predictions (
              {photoTestData.files.length} images)
            </Text>
          </Row>
          <DatasetGrid
            dir="assets/predictions/photo/test/ukiyoe/authors"
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

export default PhotoTestToUkiyoeAuthorsDatasetPage;
