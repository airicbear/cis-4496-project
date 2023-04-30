import { Collapse, Container, Grid, Spacer } from "@nextui-org/react";
import { NextPage } from "next";
import Head from "next/head";
import AppHeader from "../components/AppHeader";
import CardLink from "../components/CardLink";
import GeneratorCardLinkGrid from "../components/GeneratorCardLinkGrid";
import { painting2PaintingList } from "../consts/painting2PaintingList";
import { painting2PhotoList } from "../consts/painting2PhotoList";
import { photo2PaintingList } from "../consts/photo2PaintingList";

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
          <Collapse title="Data">
            <Grid.Container gap={2} justify="flex-start">
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/photo/test/2014-08-01 17:41:55.jpg"
                  title="Photo Test"
                  url="/datasets/photo/test"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/photo/train/2013-11-08 16:45:24.jpg"
                  title="Photo Train"
                  url="/datasets/photo/train"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/monet/test/00010.jpg"
                  title="Monet Test"
                  url="/datasets/monet/test"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/monet/train/00001.jpg"
                  title="Monet Train"
                  url="/datasets/monet/train"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/ukiyoe/test/01200.jpg"
                  title="Ukiyoe Test"
                  url="/datasets/ukiyoe/test"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/ukiyoe/train/00002.jpg"
                  title="Ukiyoe Train"
                  url="/datasets/ukiyoe/train"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/cezanne/test/00010.jpg"
                  title="Cezanne Test"
                  url="/datasets/cezanne/test"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/cezanne/train/00001.jpg"
                  title="Cezanne Train"
                  url="/datasets/cezanne/train"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/datasets/vangogh/test-train/00001.jpg"
                  title="Vangogh Test/Train"
                  url="/datasets/vangogh/test-train"
                  fontSize="14px"
                />
              </Grid>
            </Grid.Container>
          </Collapse>
          <Collapse title="Predictions">
            <Grid.Container gap={2} justify="flex-start">
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/photo/test/monet/authors/2014-08-01 17:41:55.png"
                  title="Author's Test Photo → Monet"
                  url="/predictions/photo/test/monet/authors"
                  fontSize="12px"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/monet/test/photo/authors/00010.png"
                  title="Author's Test Monet → Photo"
                  url="/predictions/monet/test/photo/authors"
                  fontSize="12px"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/photo/test/monet/ours/competition/final/2014-08-01 17:41:55.jpg"
                  title="Our Test Photo → Monet (Competition, Final)"
                  url="/predictions/photo/test/monet/ours/competition/final"
                  fontSize="12px"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/monet/test/photo/ours/competition/final/00010.jpg"
                  title="Our Test Monet → Photo (Competition, Final)"
                  url="/predictions/monet/test/photo/ours/competition/final"
                  fontSize="12px"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/photo/test/monet/ours/general/2014-08-01 17:41:55.jpg"
                  title="Our Test Photo → Monet (General)"
                  url="/predictions/photo/test/monet/ours/general"
                  fontSize="12px"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/monet/test/photo/ours/general/00010.jpg"
                  title="Our Test Monet → Photo (General)"
                  url="/predictions/monet/test/photo/ours/general"
                  fontSize="12px"
                />
              </Grid>
              <Grid xs={6} sm={3}>
                <CardLink
                  img="/assets/predictions/photo/test/ukiyoe/authors/2014-08-01 17:41:55.png"
                  title="Author's Test Photo → Ukiyoe"
                  url="/predictions/photo/test/ukiyoe/authors"
                  fontSize="12px"
                />
              </Grid>
            </Grid.Container>
          </Collapse>
          <Collapse title="Utilities">
            <Grid.Container gap={2} justify="flex-start">
              <Grid xs={6} sm={4}>
                <CardLink
                  img="/assets/images/RGB.png"
                  title="Plot RGB Distribution"
                  url="/utilities/plot_rgb_distribution"
                />
              </Grid>
              <Grid xs={6} sm={4}>
                <CardLink
                  img="/assets/images/AugmentImage.jpg"
                  title="Augment Image"
                  url="/utilities/augment_image"
                />
              </Grid>
            </Grid.Container>
          </Collapse>
        </Collapse.Group>
        <Spacer y={4} />
      </Container>
    </>
  );
};

export default Home;
