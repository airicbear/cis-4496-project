import { Card, Container, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import AppHeader from "../components/AppHeader";
import ModelCard from "../components/ModelCard";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Photo ⇆ Painting</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm alignContent="center">
        <AppHeader />
        <Card>
          <Card.Header>
            <Text h3>Generators</Text>
          </Card.Header>
          <Card.Body>
            <Text h4>Photo → Painting</Text>
            <Link href="/generators/photo2monet">Photo2Monet Generators</Link>
            <Link href="/generators/photo2ukiyoe">Photo2Ukiyoe Generators</Link>
            <Link href="/generators/photo2cezanne">
              Photo2Cezanne Generators
            </Link>
            <Link href="/generators/photo2vangogh">
              Photo2Vangogh Generators
            </Link>
            <Spacer y={2} />
            <Text h4>Painting → Photo</Text>
            <Link href="/generators/monet2photo">Monet2Photo Generators</Link>
            <Link href="/generators/ukiyoe2photo">Ukiyoe2Photo Generators</Link>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
};

export default Home;
