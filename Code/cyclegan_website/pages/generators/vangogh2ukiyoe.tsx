import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import Model2ModelCard from "../../components/Model2ModelCard";

const Vangogh2UkiyoePage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Model2ModelCard
        title="Our Vangogh2Ukiyoe Generator"
        model1Type="our-vangogh2photo"
        model2Type="our-photo2ukiyoe"
        model1URL="/assets/models/our_model/vangogh/painting2photo.json"
        model2URL="/assets/models/our_model/ukiyoe/photo2painting.json"
        model1Format="tfjs"
        model2Format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Vangogh2UkiyoePage;
