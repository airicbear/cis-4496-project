import * as Jimp from "jimp";
import { Tensor } from "onnxruntime-web";

export async function getImageTensorFromPath(
  path: string,
  dims: number[] = [1, 3, 256, 256]
): Promise<Tensor> {
  var image = await loadImageFromPath(path, dims[2], dims[3]);
  var imageTensor = imageDataToTensor(image, dims);
  return imageTensor;
}

async function loadImageFromPath(
  path: string,
  width: number = 256,
  height: number = 256
): Promise<Jimp> {
  var imageData = await Jimp.default.read(path).then((imageBuffer: Jimp) => {
    return imageBuffer.resize(width, height);
  });

  return imageData;
}

function imageDataToTensor(image: Jimp, dims: number[]): Tensor {
  var imageBufferData = image.bitmap.data;
  const [redArray, greenArray, blueArray] = new Array(
    new Array<number>(),
    new Array<number>(),
    new Array<number>()
  );
  for (let i = 0; i < imageBufferData.length; i += 4) {
    redArray.push(imageBufferData[i]);
    greenArray.push(imageBufferData[i + 1]);
    blueArray.push(imageBufferData[i + 2]);
  }

  const transposedData = redArray.concat(greenArray).concat(blueArray);

  let i: number;
  let l = transposedData.length;
  const float32Data = new Float32Array(dims[1] * dims[2] * dims[3]);
  for (i = 0; i < l; i++) {
    float32Data[i] = transposedData[i] / 255.0;
  }
  const inputTensor = new Tensor("float32", float32Data, dims);
  return inputTensor;
}
