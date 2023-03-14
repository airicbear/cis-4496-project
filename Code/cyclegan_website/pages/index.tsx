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
        <ModelCard title="Photo2Monet Generator" type="photo2painting" />
        <Spacer y={2} />
        <ModelCard title="Monet2Photo Generator" type="painting2photo" />
        <Spacer y={2} />
      </Container>
    </>
  );
};

export default Home;
