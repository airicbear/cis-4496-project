import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { photoTestData } from "../../../consts/photoTestData";

const PhotoTestDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Photo Test Data Set</Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/photo/test"
          filenames={photoTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PhotoTestDatasetPage;
