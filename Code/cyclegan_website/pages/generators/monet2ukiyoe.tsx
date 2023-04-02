import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import AppHeader from "../../components/AppHeader";
import Model2ModelCard from "../../components/Model2ModelCard";

const Monet2UkiyoePage: NextPage = () => {
  return (
    <Container sm>
      <AppHeader />
      <Model2ModelCard
        title="Author's Monet2Ukiyoe Generator"
        model1Type="author-monet2photo"
        model2Type="author-monet2photo"
        model1URL="/assets/models/authors/monet2photo.onnx"
        model2URL="/assets/models/authors/photo2ukiyoe.onnx"
        model1Format="onnx"
        model2Format="onnx"
      />
      <Spacer y={2} />
    </Container>
  );
};

export default Monet2UkiyoePage;
