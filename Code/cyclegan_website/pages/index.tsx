import {
  Col,
  Collapse,
  Container,
  Grid,
  Link,
  Row,
  Spacer,
  Text,
} from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../components/AppHeader";
import GeneratorCardLinkGrid from "../components/GeneratorCardLinkGrid";
import { photo2PaintingList } from "../consts/photo2PaintingList";
import { painting2PhotoList } from "../consts/painting2PhotoList";
import { painting2PaintingList } from "../consts/painting2PaintingList";
import CardLink from "../components/CardLink";

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>Photo ⇆ Painting</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container sm alignContent="center">
        <AppHeader />
        <Collapse.Group splitted>
          <Collapse title="Photo → Painting" expanded>
            <GeneratorCardLinkGrid list={photo2PaintingList} xs={6} sm={3} />
          </Collapse>
          <Collapse title="Painting → Photo">
            <GeneratorCardLinkGrid list={painting2PhotoList} xs={6} sm={3} />
          </Collapse>
          <Collapse title="Painting → Painting">
            <GeneratorCardLinkGrid list={painting2PaintingList} xs={4} sm={4} />
          </Collapse>
          <Collapse title="Utilities">
            <Grid.Container gap={2} justify="flex-start">
              <Grid xs={4} sm={4}>
                <CardLink
                  img="/assets/images/RGB.png"
                  title="Plot RGB Distribution"
                  url="/utilities/plot_rgb_distribution"
                />
              </Grid>
            </Grid.Container>
          </Collapse>
        </Collapse.Group>
      </Container>
    </>
  );
};

export default Home;
