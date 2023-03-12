import { Container } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../components/AppHeader";
import FileUpload from "../components/FileUpload";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Photo ⇆ Painting</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container style={{ maxWidth: "800" }}>
        <AppHeader />
        <FileUpload />
      </Container>
    </>
  );
};

export default Home;
