import { Card, FormElement, Input, Text, useTheme } from "@nextui-org/react";
import { ChangeEvent } from "react";
import * as ort from "onnxruntime-web";

interface ImageInputProps {
  type: string;
}

const onnxModelURL = "/assets/models/netG_A.onnx";
const sessionOption = { executionProviders: ["wasm"] };

async function createInferenceSession(onnxModelURL, sessionOption) {
  let session: ort.InferenceSession;

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

var inferenceSession: ort.InferenceSession;
async function submitInference(imageTensor: ort.Tensor) {
  console.log("Submitting inference on image tensor...");
  inferenceSession = await createInferenceSession(onnxModelURL, sessionOption);
  return await runInference(inferenceSession, imageTensor);
}

const ImageInput = ({ type }: ImageInputProps) => {
  const { theme } = useTheme();

  const outputPrediction = async (reader: FileReader) => {
    const canvas = document.getElementById(type) as HTMLCanvasElement;
    canvas.style.borderRadius = `${theme.radii.lg.value}`;
    const image = new Image();
    image.src = reader.result.toString();
    image.style.borderRadius = `${theme.radii.lg.value}`;
    image.onload = async () => {
      try {
        console.log("Converting image to tensor...");
        const imageTensor: ort.Tensor = await (
          ort.Tensor as unknown as ort.TensorFactory
        ).fromImage(image.src, {
          tensorFormat: "RGB",
          resizedWidth: 256,
          resizedHeight: 256,
        });
        console.log("Finished converting image to tensor.");
        console.log(imageTensor);

        submitInference(imageTensor).then((result) => {
          const output = result[inferenceSession.outputNames[0]];
          console.log("Inference complete.");
          console.log(output);

          console.log("Processing output...");
          const float32Data = new Float32Array(output.data.length);
          for (let i = 0; i < output.data.length; i++) {
            float32Data[i] = output.data[i] * 0.5 + 0.5;
          }
          console.log(float32Data);

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
    };
  };

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const label = document.getElementById(`label-file-upload-${type}`);
    const file = files[0];
    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        label.style.backgroundImage = `url(${reader.result})`;
        label.style.backgroundSize = "256px 256px";
        label.style.backgroundRepeat = "no-repeat";
        label.textContent = "";
        outputPrediction(reader);
      },
      false
    );
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const setLabelTransparency = function (alpha: number) {
    const label = document.getElementById(`label-file-upload-${type}`);
    label.style.opacity = `${alpha}`;
  };

  const setLabelBackgroundColor = function (color: string) {
    const label = document.getElementById(`label-file-upload-${type}`);
    label.style.backgroundColor = `${color}`;
  };

  const handleDragOver = function (event: {
    stopPropagation: () => void;
    preventDefault: () => void;
    dataTransfer: { dropEffect: string };
  }) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
    setLabelTransparency(0.5);
    setLabelBackgroundColor(`${theme.colors.neutralBorderHover.value}`);
  };

  const handleDragLeave = function (event: {
    stopPropagation: () => void;
    preventDefault: () => void;
  }) {
    event.stopPropagation();
    event.preventDefault();
    setLabelTransparency(1.0);
    setLabelBackgroundColor(`${theme.colors.neutralLight.value}`);
  };

  const handleDrop = function (event: {
    stopPropagation: () => void;
    preventDefault: () => void;
    dataTransfer: { files: any };
  }) {
    event.stopPropagation();
    event.preventDefault();
    const files = event.dataTransfer.files;
    const label = document.getElementById(`label-file-upload-${type}`);
    const file = files[0];
    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        label.style.backgroundImage = `url(${reader.result})`;
        label.style.backgroundSize = "256px 256px";
        label.style.backgroundRepeat = "no-repeat";
        label.textContent = "";
        outputPrediction(reader);
      },
      false
    );
    if (file) {
      reader.readAsDataURL(file);
    }
    setLabelTransparency(1.0);
    setLabelBackgroundColor(`${theme.colors.neutralLight.value}`);
  };

  return (
    <form style={{ textAlign: "center" }}>
      <Input
        type="file"
        id={`input-file-upload-${type}`}
        accept=".jpg, .jpeg, .png"
        onChange={handleChange}
        css={{
          display: "none",
        }}
      ></Input>

      <label
        htmlFor={`input-file-upload-${type}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDragEnd={handleDragLeave}
        onDrop={handleDrop}
        style={{
          display: "inline-flex",
          textAlign: "center",
        }}
      >
        <Card
          css={{
            bg: `${theme.colors.neutralLight.value}`,
          }}
        >
          <Card.Body
            id={`label-file-upload-${type}`}
            css={{
              width: "256px",
              height: "256px",
              textAlign: "center",
              verticalAlign: "center",
              display: "flex",
              justifyContent: "center",
              alignContent: "center",
              flexDirection: "column",
              "@media (max-width: 620px)": {
                width: "128px",
                height: "128px",
                backgroundSize: "128px 128px",
              },
            }}
          >
            <Text
              h3
              css={{
                "@media (max-width: 620px)": {
                  fontSize: "12px",
                },
              }}
            >
              Upload image
            </Text>
            <Text
              css={{
                "@media (max-width: 620px)": {
                  fontSize: "12px",
                },
              }}
            >
              (Click or Drag/Drop)
            </Text>
          </Card.Body>
        </Card>
      </label>
    </form>
  );
};

export default ImageInput;
