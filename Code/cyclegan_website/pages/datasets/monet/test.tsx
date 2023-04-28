import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";

const MonetTestDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Monet Test Data Set</Text>
        </Row>
        <DatasetGrid dir="assets/datasets/monet/test" />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default MonetTestDatasetPage;
