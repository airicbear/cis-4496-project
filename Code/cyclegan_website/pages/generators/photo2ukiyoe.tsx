import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Photo2UkiyoePage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Author's Photo2Ukiyoe Generator"
        type="author-photo2ukiyoe"
        modelURL="/assets/models/authors/photo2ukiyoe.onnx"
        format="onnx"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Photo2Ukiyoe Generator"
        type="our-photo2ukiyoe"
        modelURL="/assets/models/our_model/ukiyoe/photo2painting/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Photo2UkiyoePage;
