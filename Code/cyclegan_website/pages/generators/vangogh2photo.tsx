import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Vangogh2PhotoPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Our Vangogh2Photo Generator"
        type="our-vangogh2photo"
        modelURL="/assets/models/our_model/vangogh/painting2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Vangogh2PhotoPage;
