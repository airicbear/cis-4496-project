import { Grid, Image } from "@nextui-org/react";

interface DatasetGridProps {
  dir: string;
  filenames: string[];
}

const DatasetGrid = ({ dir, filenames }: DatasetGridProps) => {
  return (
    <Grid.Container justify="flex-start">
      {filenames.map((file) => (
        <Grid xs={3} sm={2} key={file}>
          <Image src={`/${dir}/${file}`} key={`/${dir}/${file}`} />
        </Grid>
      ))}
    </Grid.Container>
  );
};

export default DatasetGrid;
