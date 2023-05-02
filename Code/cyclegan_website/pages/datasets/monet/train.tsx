import { Container, Row, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../../components/AppHeader";
import DatasetGrid from "../../../components/DatasetGrid";
import { monetTrainData } from "../../../consts/monetTrainData";

const MonetTrainDatasetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>
            Monet Train Data Set ({monetTrainData.files.length} images)
          </Text>
        </Row>
        <DatasetGrid
          dir="assets/datasets/monet/train"
          filenames={monetTrainData.files}
        />
        <Spacer y={2} />
      </Container>
    </Container>
  );
};

export default MonetTrainDatasetPage;
