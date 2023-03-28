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
        title="Our Monet2Photo Generator"
        type="our-monet2photo"
        modelURL="/assets/models/our_model/monet2photo/model.json"
        format="tfjs"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Monet2PhotoPage;
