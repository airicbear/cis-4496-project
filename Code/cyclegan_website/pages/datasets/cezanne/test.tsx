import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { cezanneTestData } from "../../../consts/cezanneTestData";

const CezanneTestDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Cezanne Test Data Set</Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/cezanne/test"
          filenames={cezanneTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default CezanneTestDatasetPage;
