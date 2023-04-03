import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import Model2ModelCard from "../../components/Model2ModelCard";

const Cezanne2UkiyoePage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Model2ModelCard
        title="Our Cezanne2Ukiyoe Generator"
        model1Type="our-cezanne2photo"
        model2Type="our-photo2ukiyoe"
        model1URL="/assets/models/our_model/cezanne/painting2photo/model.json"
        model2URL="/assets/models/our_model/ukiyoe/photo2painting/model.json"
        model1Format="tfjs"
        model2Format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Cezanne2UkiyoePage;
