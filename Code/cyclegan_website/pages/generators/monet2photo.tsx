import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import ModelCard from "../../components/ModelCard";

const Monet2PhotoPage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <ModelCard
        title="Author's Monet2Photo Generator"
        type="author-monet2photo"
        modelURL="/assets/models/authors/monet2photo.onnx"
        format="onnx"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Monet2Photo Generator (Competition, Final)"
        type="our-competition-final-monet2photo"
        modelURL="/assets/models/our_model/monet-competition-final/painting2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Monet2Photo Generator (Competition, V2)"
        type="our-competition-v2-monet2photo"
        modelURL="/assets/models/our_model/monet-competition-v2/painting2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
      <ModelCard
        title="Our Monet2Photo Generator (Generic)"
        type="our-monet2photo"
        modelURL="/assets/models/our_model/monet/painting2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Monet2PhotoPage;
