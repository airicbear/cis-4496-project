import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { cezanneTrainData } from "../../../consts/cezanneTrainData";

const CezanneTrainDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Cezanne Train Data Set</Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/cezanne/train"
          filenames={cezanneTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default CezanneTrainDatasetPage;
