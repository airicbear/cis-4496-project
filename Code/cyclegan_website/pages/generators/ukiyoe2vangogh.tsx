import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import Model2ModelCard from "../../components/Model2ModelCard";

const Ukiyoe2VangoghPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Model2ModelCard
        title="Our Ukiyoe2Vangogh Generator"
        model1Type="our-ukiyoe2photo"
        model2Type="our-photo2vangogh"
        model1URL="/assets/models/our_model/ukiyoe/painting2photo/model.json"
        model2URL="/assets/models/our_model/vangogh/photo2painting/model.json"
        model1Format="tfjs"
        model2Format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Ukiyoe2VangoghPage;
