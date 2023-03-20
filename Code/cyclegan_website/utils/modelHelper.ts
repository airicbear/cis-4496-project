import * as ort from "onnxruntime-web";

export async function runCycleganModel(
  preprocessedData: any
): Promise<[any, number]> {
  const session = await ort.InferenceSession.create(
    "/public/assets/models/netG_A.onnx",
    { executionProviders: ["webgl"], graphOptimizationLevel: "all" }
  );
  console.log("Inference session created");
  var [results, inferenceTime] = await runInference(session, preprocessedData);
  return [results, inferenceTime];
}

async function runInference(
  session: ort.InferenceSession,
  preprocessedData: any
): Promise<[any, number]> {
  const start = new Date();
  const feeds: Record<string, ort.Tensor> = {};
  feeds[session.inputNames[0]] = preprocessedData;
  const outputData = await session.run(feeds);
  const end = new Date();
  const inferenceTime = (end.getTime() - start.getTime()) / 1000;
  const output = outputData[session.outputNames[0]];
  console.log("results: ", output);
  return [output, inferenceTime];
}
