import { Card, FormElement, Input, Text, useTheme } from "@nextui-org/react";
import * as tf from "@tensorflow/tfjs";
import * as ort from "onnxruntime-web";
import { ChangeEvent } from "react";
import {
  createInferenceSession,
  drawOnnxPrediction,
} from "../utils/drawOnnxPrediction";
import { drawTfjsPrediction, getTfjsModel } from "../utils/drawTfjsPrediction";

interface ImageInputProps {
  type: string;
  modelURL: string;
  format: string;
}

const ImageInput = ({ type, modelURL, format }: ImageInputProps) => {
  const { theme } = useTheme();
  let tfModel: tf.GraphModel;
  let inferenceSession: ort.InferenceSession;
  const sessionOptions = { executionProviders: ["wasm"] };

  if (format == "tfjs" && tfModel == null) {
    getTfjsModel(modelURL).then((model: tf.GraphModel) => {
      tfModel = model;
      console.log("Done loading TensorFlow.js model.");
    });
  }

  const drawPrediction = async (reader: FileReader) => {
    const canvas = document.getElementById(type) as HTMLCanvasElement;
    canvas.style.borderRadius = `${theme.radii.lg.value}`;

    const image = new Image();
    image.src = reader.result.toString();
    image.style.borderRadius = `${theme.radii.lg.value}`;
    image.onload = async () => {
      if (format == "onnx") {
        if (inferenceSession == null) {
          inferenceSession = await createInferenceSession(
            modelURL,
            sessionOptions
          );
        }

        drawOnnxPrediction(
          canvas,
          image,
          inferenceSession,
          modelURL,
          sessionOptions
        );
      } else if (format == "tfjs") {
        drawTfjsPrediction(tfModel, canvas, image);
      } else {
        console.error(`Invalid format "${format}"`);
      }
    };
  };

  const initializeLabel = function (
    label: HTMLElement,
    backgroundImage: string
  ) {
    label.style.backgroundImage = backgroundImage;
    label.style.backgroundSize = "256px 256px";
    label.style.backgroundRepeat = "no-repeat";
    label.textContent = "";
  };

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const label = document.getElementById(`label-file-upload-${type}`);

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const file = files[0];

    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        initializeLabel(label, `url(${reader.result})`);
        drawPrediction(reader);
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

    const label = document.getElementById(`label-file-upload-${type}`);

    const files = event.dataTransfer.files;
    const file = files[0];

    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        initializeLabel(label, `url(${reader.result})`);
        drawPrediction(reader);
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
