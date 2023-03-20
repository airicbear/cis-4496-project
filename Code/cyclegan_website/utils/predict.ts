import { getImageTensorFromPath } from "./imageHelper";
import { runCycleganModel } from "./modelHelper";

export async function inferenceCyclegan(path: string): Promise<[any, number]> {
  const imageTensor = await getImageTensorFromPath(path);
  const [predictions, inferenceTime] = await runCycleganModel(imageTensor);
  return [predictions, inferenceTime];
}
