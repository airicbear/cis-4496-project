import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { photoTrainData } from "../../../consts/photoTrainData";

const PhotoTrainDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Photo Train Data Set</Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/photo/train"
          filenames={photoTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default PhotoTrainDatasetPage;
