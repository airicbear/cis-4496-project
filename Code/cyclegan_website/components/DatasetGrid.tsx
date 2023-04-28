import { Grid, Image } from "@nextui-org/react";
import { useEffect, useState } from "react";

interface DatasetGridProps {
  dir: string;
  limit: string;
  offset: string;
}

const DatasetGrid = ({ dir, limit, offset }: DatasetGridProps) => {
  const [files, setFiles] = useState<string[]>([]);

  async function fetchFiles(dir: string) {
    const res = await fetch(
      `/api/get-files?dir=${dir}&limit=${limit}&offset=${offset}`
    );
    const data = await res.json();
    return data.files;
  }

  useEffect(() => {
    if (files.length == 0) {
      fetchFiles(dir).then((files) => setFiles(files));
    }
  });

  return (
    <Grid.Container justify="flex-start">
      {files.map((file) => (
        <Grid xs={3} sm={2}>
          <Image src={`/${dir}/${file}`} key={`/${dir}/${file}`} />
        </Grid>
      ))}
    </Grid.Container>
  );
};

export default DatasetGrid;
