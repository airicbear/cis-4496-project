import { Card, Container, Spacer, Text } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import AppHeader from "../components/AppHeader";

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
            <Spacer y={1} />
            <Text h4>Painting → Photo</Text>
            <Link href="/generators/monet2photo">Monet2Photo Generators</Link>
            <Link href="/generators/ukiyoe2photo">Ukiyoe2Photo Generators</Link>
            <Link href="/generators/cezanne2photo">
              Cezanne2Photo Generators
            </Link>
            <Link href="/generators/vangogh2photo">
              Vangogh2Photo Generators
            </Link>
            <Spacer y={1} />
            <Text h4>Painting → Painting</Text>
            <Link href="/generators/monet2ukiyoe">Monet2Ukiyoe Generators</Link>
            <Link href="/generators/monet2cezanne">
              Monet2Cezanne Generators
            </Link>
            <Link href="/generators/monet2vangogh">
              Monet2Vangogh Generators
            </Link>
            <Link href="/generators/ukiyoe2monet">Ukiyoe2Monet Generators</Link>
            <Link href="/generators/ukiyoe2cezanne">
              Ukiyoe2Cezanne Generators
            </Link>
            <Link href="/generators/ukiyoe2vangogh">
              Ukiyoe2Vangogh Generators
            </Link>
            <Link href="/generators/cezanne2monet">
              Cezanne2Monet Generators
            </Link>
            <Link href="/generators/cezanne2ukiyoe">
              Cezanne2Ukiyoe Generators
            </Link>
            <Link href="/generators/cezanne2vangogh">
              Cezanne2Vangogh Generators
            </Link>
            <Link href="/generators/vangogh2monet">
              Vangogh2Monet Generators
            </Link>
            <Link href="/generators/vangogh2ukiyoe">
              Vangogh2Ukiyoe Generators
            </Link>
            <Link href="/generators/vangogh2cezanne">
              Vangogh2Cezanne Generators
            </Link>
          </Card.Body>
        </Card>
        <Spacer y={1} />
        <Card>
          <Card.Header>
            <Text h3>Utilities</Text>
          </Card.Header>
          <Card.Body>
            <Text h4>Data Acquisition and Understanding</Text>
            <Link href="/utilities/plot_rgb_distribution">
              Plot RGB Distribution
            </Link>
          </Card.Body>
        </Card>
      </Container>
    </>
  );
};

export default Home;
