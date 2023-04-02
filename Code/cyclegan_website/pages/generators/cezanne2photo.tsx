import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Cezanne2PhotoPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Our Cezanne2Photo Generator"
        type="our-cezanne2photo"
        modelURL="/assets/models/our_model/cezanne/painting2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Cezanne2PhotoPage;
