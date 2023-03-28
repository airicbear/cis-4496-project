import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Ukiyoe2PhotoPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Our Ukiyoe2Photo Generator"
        type="our-ukiyoe2photo"
        modelURL="/assets/models/our_model/ukiyoe2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Ukiyoe2PhotoPage;
