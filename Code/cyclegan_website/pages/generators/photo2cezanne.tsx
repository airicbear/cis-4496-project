import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Photo2CezannePage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Author's Photo2Cezanne Generator"
        type="author-photo2cezanne"
        modelURL="/assets/models/authors/photo2cezanne.ort"
        format="onnx"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Photo2Cezanne Generator"
        type="our-photo2cezanne"
        modelURL="/assets/models/our_model/cezanne/photo2painting/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Photo2CezannePage;
