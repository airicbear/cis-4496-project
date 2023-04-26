import { InferenceSession, Tensor, TensorFactory } from "onnxruntime-web";

export async function createInferenceSession(
  onnxModelURL: string,
  sessionOption: InferenceSession.SessionOptions
) {
  let session: InferenceSession | undefined;

  console.log("Creating inference session...");
  try {
    session = await InferenceSession.create(onnxModelURL, sessionOption);
  } catch (e) {
    console.error(`Failed to load ONNX model: ${e}.`);
  }

  return session;
}

async function runInference(
  session: InferenceSession,
  imageTensor: Tensor
): Promise<InferenceSession.OnnxValueMapType> {
  const feeds: Record<string, Tensor> = {};
  feeds[session.inputNames[0]] = imageTensor;

  console.log("Running inference...");
  const outputData = session.run(feeds);

  return outputData;
}

export async function drawOnnxPrediction(
  inferenceSession: InferenceSession,
  canvas: HTMLCanvasElement,
  dataURI: string
) {
  try {
    console.log("Converting image to tensor...");
    const imageTensor: Tensor = await (
      Tensor as unknown as TensorFactory
    ).fromImage(dataURI, {
      tensorFormat: "RGB",
      resizedWidth: 256,
      resizedHeight: 256,
    });
    console.log(imageTensor);

    runInference(inferenceSession, imageTensor).then((result) => {
      const output = result[inferenceSession.outputNames[0]];
      console.log("Inference complete.");
      console.log(output);

      console.log("Processing output...");
      const float32Data = new Float32Array(output.data.length);
      for (let i = 0; i < output.data.length; i++) {
        float32Data[i] = (output.data[i] as number) * 0.5 + 0.5;
      }

      const outputTensor = new Tensor("float32", float32Data, [1, 3, 256, 256]);
      console.log(outputTensor);

      const imageHTML = outputTensor.toImageData();
      const context = canvas.getContext("2d");
      context?.putImageData(imageHTML, 0, 0);
    });
  } catch (e) {
    console.error(`Failed to inference ONNX model: ${e}.`);
  }
}
