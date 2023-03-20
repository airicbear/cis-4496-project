import { Container, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../components/AppHeader";
import ModelCard from "../components/ModelCard";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Photo ⇆ Painting</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container>
        <AppHeader />
        <ModelCard
          title="Author's Photo2Monet Generator"
          type="photo2painting"
          modelURL="/assets/models/authors/photo2monet.onnx"
          format="onnx"
        />
        <Spacer y={2} />
        <ModelCard
          title="Our Photo2Monet Generator"
          type="painting2photo"
          modelURL="/assets/models/our_model/photo2painting/model.json"
          format="tfjs"
        />
        <Spacer y={2} />
      </Container>
    </>
  );
};

export default Home;
