import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import Model2ModelCard from "../../components/Model2ModelCard";

const Monet2CezannePage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Model2ModelCard
        title="Author's Monet2Cezanne Generator"
        model1Type="author-monet2photo"
        model2Type="author-photo2cezanne"
        model1URL="/assets/models/authors/monet2photo.onnx"
        model2URL="/assets/models/authors/photo2cezanne.onnx"
        model1Format="onnx"
        model2Format="onnx"
      />
      <Spacer y={2} />
      <Model2ModelCard
        title="Our Monet2Cezanne Generator"
        model1Type="our-monet2photo"
        model2Type="our-photo2cezanne"
        model1URL="/assets/models/our_model/monet/painting2photo.json"
        model2URL="/assets/models/our_model/cezanne/photo2painting.json"
        model1Format="tfjs"
        model2Format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Monet2CezannePage;
