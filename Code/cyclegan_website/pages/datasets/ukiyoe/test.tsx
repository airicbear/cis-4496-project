import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { ukiyoeTestData } from "../../../consts/ukiyoeTestData";

const UkiyoeTestDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>
            Ukiyoe Test Data Set ({ukiyoeTestData.files.length} images)
          </Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/ukiyoe/test"
          filenames={ukiyoeTestData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default UkiyoeTestDatasetPage;
