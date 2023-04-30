import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../../../../components/AppHeader";
import DatasetGrid from "../../../../../../../components/DatasetGrid";
import { photoTestData } from "../../../../../../../consts/photoTestData";
import Head from "next/head";

const PhotoTestToMonetOursCompetitionFinalDatasetPage: NextPage = () => {
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
            <Text h3>
              Our Test Photo to Monet Predictions (Competition, Final)
            </Text>
          </Row>
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
