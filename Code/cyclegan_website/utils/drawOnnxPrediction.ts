import * as ort from "onnxruntime-web";

export async function createInferenceSession(
  onnxModelURL: string,
  sessionOption: ort.InferenceSession.SessionOptions
) {
  let session: ort.InferenceSession;

  console.log("Creating inference session...");
  try {
    session = await ort.InferenceSession.create(onnxModelURL, sessionOption);
  } catch (e) {
    console.error(`Failed to load ONNX model: ${e}.`);
  }

  return session;
}

async function runInference(
  session: ort.InferenceSession,
  imageTensor: ort.Tensor
): Promise<ort.InferenceSession.OnnxValueMapType> {
  const feeds: Record<string, ort.Tensor> = {};
  feeds[session.inputNames[0]] = imageTensor;

  console.log("Running inference...");
  const outputData = session.run(feeds);

  return outputData;
}

function imageToDataUri(img: HTMLImageElement, width: number, height: number) {
  let canvas = document.createElement("canvas");
  let ctx = canvas.getContext("2d");

  canvas.width = width;
  canvas.height = height;

  ctx.drawImage(img, 0, 0, width, height);

  return canvas.toDataURL("image/jpeg", 1.0);
}

export async function drawOnnxPrediction(
  inferenceSession: ort.InferenceSession,
  canvas: HTMLCanvasElement,
  image: HTMLImageElement
) {
  try {
    console.log("Converting image to tensor...");
    const imageTensor: ort.Tensor = await (
      ort.Tensor as unknown as ort.TensorFactory
    ).fromImage(imageToDataUri(image, 256, 256), {
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

      const outputTensor = new ort.Tensor(
        "float32",
        float32Data,
        [1, 3, 256, 256]
      );
      console.log(outputTensor);

      const imageHTML = outputTensor.toImageData();
      const context = canvas.getContext("2d");
      context.putImageData(imageHTML, 0, 0);
    });
  } catch (e) {
    console.error(`Failed to inference ONNX model: ${e}.`);
  }
}
