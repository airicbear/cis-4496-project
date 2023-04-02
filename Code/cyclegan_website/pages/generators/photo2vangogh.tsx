import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Photo2VangoghPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Author's Photo2Vangogh Generator"
        type="author-photo2vangogh"
        modelURL="/assets/models/authors/photo2vangogh.onnx"
        format="onnx"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Photo2Vangogh Generator"
        type="our-photo2vangogh"
        modelURL="/assets/models/our_model/vangogh/photo2painting/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Photo2VangoghPage;
