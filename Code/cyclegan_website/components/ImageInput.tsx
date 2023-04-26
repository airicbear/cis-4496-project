import { FormElement, Input, Loading, useTheme } from "@nextui-org/react";
import { GraphModel } from "@tensorflow/tfjs";
import { InferenceSession } from "onnxruntime-web";
import { ChangeEvent, MutableRefObject, useEffect, useState } from "react";
import {
  createInferenceSession,
  drawOnnxPrediction,
} from "../utils/drawOnnxPrediction";
import { drawTfjsPrediction, getTfjsModel } from "../utils/drawTfjsPrediction";
import { imageToDataUri } from "../utils/imageToDataUri";
import { initializeLabel } from "../utils/initializeLabel";
import ImageInputLabel from "./ImageInputLabel";

interface ImageInputProps {
  type: string;
  modelURL: string;
  format: string;
  onRunInference: Function;
  canvasRef: MutableRefObject<HTMLCanvasElement>;
  labelRef: MutableRefObject<HTMLLabelElement>;
}

const ImageInput = ({
  type,
  modelURL,
  format,
  onRunInference,
  canvasRef,
  labelRef,
}: ImageInputProps) => {
  const { theme } = useTheme();
  const [tfModel, setTfModel] = useState<GraphModel | null>(null);
  const [inferenceSession, setInferenceSession] =
    useState<InferenceSession | null>(null);
  const sessionOptions = { executionProviders: ["wasm"] };

  if (format == "tfjs" && tfModel == null) {
    const indexedDBURL = `indexeddb://${type}`;

    getTfjsModel(indexedDBURL).then(
      (model: GraphModel) => {
        setTfModel(model);

        console.log(
          `(${type}) Loaded TensorFlow.js model from IndexedDB (${indexedDBURL}).`
        );
      },
      () => {
        getTfjsModel(modelURL).then(
          async (model: GraphModel) => {
            setTfModel(model);

            await model.save(indexedDBURL);

            console.log(
              `(${type}) Saved TensorFlow.js model to IndexedDB (${indexedDBURL}).`
            );
          },
          () => {
            console.error(`(${type}) Failed to load model from ${modelURL}.`);
          }
        );
      }
    );
  }

  useEffect(() => {
    if (format == "onnx" && inferenceSession == null) {
      createInferenceSession(modelURL, sessionOptions).then(
        (session: InferenceSession | undefined) => {
          if (session) {
            setInferenceSession(session);
          }
          console.log(`(${type}) Done loading ONNX model.`);
        }
      );
    }
  });

  const drawPrediction = async (reader: FileReader) => {
    const image = new Image();
    if (reader.result) {
      image.src = reader.result.toString();
    }
    if (theme) {
      image.style.borderRadius = `${theme.radii.lg.value}`;
    }
    image.onload = async () => {
      if (format == "onnx") {
        if (inferenceSession != null) {
          onRunInference(true);
          drawOnnxPrediction(
            inferenceSession,
            canvasRef.current,
            imageToDataUri(image, 256, 256)
          ).then(() => {
            onRunInference(false);
          });
        } else {
          console.error(`(${type}) Model not yet loaded.`);
        }
      } else if (format == "tfjs") {
        if (tfModel != null) {
          onRunInference(true);
          drawTfjsPrediction(tfModel, canvasRef.current, image).then(() => {
            onRunInference(false);
          });
        } else {
          console.error(`(${type}) Model not yet loaded.`);
        }
      } else {
        console.error(`Invalid format "${format}"`);
      }
    };
  };

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const file = files ? files[0] : null;

    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        initializeLabel(labelRef.current, `url(${reader.result})`);
        drawPrediction(reader);
      },
      false
    );
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  return (
    <form style={{ textAlign: "center" }}>
      <Input
        type="file"
        id={`input-file-upload-${type}`}
        accept="image/*"
        onChange={handleChange}
        css={{
          display: "none",
        }}
      ></Input>

      {(format == "onnx" && inferenceSession) ||
      (format == "tfjs" && tfModel) ? (
        <ImageInputLabel
          htmlFor={`input-file-upload-${type}`}
          onFileUpload={(reader: FileReader) => drawPrediction(reader)}
          id={`label-file-upload-${type}`}
          labelRef={labelRef}
        />
      ) : (
        <Loading size="xl" />
      )}
    </form>
  );
};

export default ImageInput;
