import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../../../../../components/AppHeader";
import DatasetGrid from "../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../consts/photoTestData";

const PhotoTestToVangoghAuthorsDatasetPage: NextPage = () => {
  return (
    <>
      <Head>
        <title>Author's Test Photo to Van Gogh Predictions</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm>
        <AppHeader />
        <Container>
          <Row align="center">
            <Text h3>Author's Test Photo to Van Gogh Predictions</Text>
          </Row>
          <DatasetGrid
            dir="assets/predictions/photo/test/vangogh/authors"
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

export default PhotoTestToVangoghAuthorsDatasetPage;
