import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../components/AppHeader";
import DatasetGrid from "../../../../components/DatasetGrid";
import { photoTestData } from "../../../../consts/photoTestData";

const PhotoTestToMonetDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Test Photo to Monet Predictions</Text>
        </Row>
        <DatasetGrid
          dir="assets/predictions/photo/test/monet"
          filenames={photoTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PhotoTestToMonetDatasetPage;
