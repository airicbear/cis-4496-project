import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { vangoghTestTrainData } from "../../../consts/vangoghTestTrainData";

const VangoghTestDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>
            Vangogh Test/Train Data Set ({vangoghTestTrainData.files.length}{" "}
            images)
          </Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/vangogh/test-train"
          filenames={vangoghTestTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default VangoghTestDatasetPage;
