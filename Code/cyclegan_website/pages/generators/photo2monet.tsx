import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Photo2MonetPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Author's Photo2Monet Generator"
        type="author-photo2monet"
        modelURL="/assets/models/authors/photo2monet.onnx"
        format="onnx"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Photo2Monet Generator (Competition)"
        type="our-competition-photo2monet"
        modelURL="/assets/models/our_model/monet-competition/photo2painting/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Photo2Monet Generator (Generic)"
        type="our-photo2monet"
        modelURL="/assets/models/our_model/monet/photo2painting/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Photo2MonetPage;
