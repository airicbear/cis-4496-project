import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";

const MonetTrainDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Monet Train Data Set</Text>
        </Row>
        <DatasetGrid dir="assets/datasets/monet/train" />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default MonetTrainDatasetPage;
