import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { ukiyoeTrainData } from "../../../consts/ukiyoeTrainData";

const UkiyoeTrainDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Ukiyoe Train Data Set</Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/ukiyoe/train"
          filenames={ukiyoeTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default UkiyoeTrainDatasetPage;
