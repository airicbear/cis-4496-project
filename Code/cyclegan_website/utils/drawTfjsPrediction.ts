import {
  browser,
  expandDims,
  GraphModel,
  loadGraphModel,
  Rank,
  squeeze,
  Tensor,
} from "@tensorflow/tfjs";

export async function drawTfjsPrediction(
  model: GraphModel,
  canvas: HTMLCanvasElement,
  image: HTMLImageElement | HTMLCanvasElement
) {
  const input = browser
    .fromPixels(image, 3)
    .toFloat()
    .mul(1 / 127.5)
    .sub(1)
    .resizeBilinear([256, 256]);

  try {
    const output: Tensor<Rank> = model.predict(
      expandDims(input, 0)
    ) as Tensor<Rank>;

    const outputTensor = output.mul(127.5).add(127.5).toInt();
    const squeezedOutput = squeeze(outputTensor, [0]).as3D(256, 256, 3);

    const context = canvas.getContext("2d");
    context?.clearRect(0, 0, canvas.width, canvas.height);
    browser.toPixels(squeezedOutput, canvas);
  } catch {
    throw new Error("Model prediction failed.");
  }
}

export async function getTfjsModel(modelURL: string) {
  return await loadGraphModel(modelURL);
}
