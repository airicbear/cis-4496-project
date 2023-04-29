import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../../components/AppHeader";
import DatasetGrid from "../../../../components/DatasetGrid";
import { monetTestData } from "../../../../consts/monetTestData";

const PhotoTestToMonetDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Test Monet to Photo Predictions (Competition, Final)</Text>
        </Row>
        <DatasetGrid
          dir="assets/predictions/monet/test/photo"
          filenames={monetTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PhotoTestToMonetDatasetPage;
