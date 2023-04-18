import { Grid } from "@nextui-org/react";
import CardLink from "./CardLink";

const GeneratorCardLinkGrid = ({ list, xs, sm }) => {
  return (
    <Grid.Container gap={2} justify="flex-start">
      {list.map((item, index: number) => (
        <Grid xs={xs} sm={sm} key={index}>
          <CardLink img={item.img} title={item.title} url={item.url} />
        </Grid>
      ))}
    </Grid.Container>
  );
};

export default GeneratorCardLinkGrid;
