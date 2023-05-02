import { useEffect } from "react";
import { plotDensity } from "../utils/plotRGB";
import { getRGB, getRGBFrequency } from "../utils/getRGB";
import { deepMergeSum } from "../utils/deepMergeSum";
import { createPlot } from "../utils/createPlot";
import { Container } from "@nextui-org/react";

interface PlotContainerProps {
  id: string;
  files: string[];
  dir: string;
}

const PlotContainer = ({ id, files, dir }: PlotContainerProps) => {
  const calcAndGraph = (imgs: HTMLImageElement[]) => {
    // Set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 50, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const plotContainer = document.getElementById(id);
    if (plotContainer) {
      plotContainer.innerHTML = "";
    }

    // Append the svg object to the body of the page
    const svg = createPlot(
      `#${id}`,
      width,
      height,
      margin,
      "RGB Distribution",
      "RGB Value",
      "Frequency"
    );

    const rgbList = imgs.map((img) => {
      return getRGB(img);
    });

    const { rD, gD, bD } = rgbList.reduce(
      (acc, obj) => (acc = deepMergeSum(acc, obj))
    );

    const rData = getRGBFrequency(rD);
    const gData = getRGBFrequency(gD);
    const bData = getRGBFrequency(bD);
    const rDataArray = rData.map<[number, number]>((d) => [d.idx, d.freq]);
    const gDataArray = gData.map<[number, number]>((d) => [d.idx, d.freq]);
    const bDataArray = bData.map<[number, number]>((d) => [d.idx, d.freq]);
    const rFreq = rData.map<number>((d) => d.freq);
    const gFreq = gData.map<number>((d) => d.freq);
    const bFreq = bData.map<number>((d) => d.freq);

    const totalFreq = rFreq.concat(gFreq).concat(bFreq);
    const maxFreq = Math.max(...totalFreq);

    plotDensity(width, height, svg, rDataArray, "red", maxFreq);
    plotDensity(width, height, svg, gDataArray, "green", maxFreq);
    plotDensity(width, height, svg, bDataArray, "blue", maxFreq);
  };

  useEffect(() => {
    const images = files.map((file) => {
      const img = new Image();
      img.src = `${dir}/${file}`;
      return img;
    });

    calcAndGraph(images);
  });

  return <Container id={id}></Container>;
};

export default PlotContainer;
