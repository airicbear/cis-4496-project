import { Col, Container, Row, Text, useTheme } from "@nextui-org/react";
import { GraphModel } from "@tensorflow/tfjs";
import { InferenceSession } from "onnxruntime-web";
import { useEffect, useRef, useState } from "react";
import {
  createInferenceSession,
  drawOnnxPrediction,
} from "../utils/drawOnnxPrediction";
import { drawTfjsPrediction, getTfjsModel } from "../utils/drawTfjsPrediction";
import CanvasOutput from "./CanvasOutput";
import ImageInput from "./ImageInput";
import ImageInputTitle from "./ImageInputTitle";

interface Model2ModelCardProps {
  title: string;
  model1Type: string;
  model2Type: string;
  model1URL: string;
  model2URL: string;
  model1Format: string;
  model2Format: string;
}

const Model2ModelCard = ({
  title,
  model1Type,
  model2Type,
  model1URL,
  model2URL,
  model1Format,
  model2Format,
}: Model2ModelCardProps) => {
  const { theme } = useTheme();
  const [tfModel, setTfModel] = useState<GraphModel | null>(null);
  const [inferenceSession, setInferenceSession] =
    useState<InferenceSession | null>(null);
  const sessionOptions = { executionProviders: ["wasm"] };
  const [isLoading, setIsLoading] = useState(false);
  const [isPredicted, setIsPredicted] = useState(false);
  const canvas1Ref = useRef<HTMLCanvasElement>(null);
  const canvas2Ref = useRef<HTMLCanvasElement>(null);
  const labelRef = useRef<HTMLDivElement>(null);

  if (model2Format == "tfjs" && tfModel == null) {
    const indexedDBURL = `indexeddb://${model2Type}`;

    getTfjsModel(indexedDBURL).then(
      (model: GraphModel) => {
        setTfModel(model);

        console.log(
          `(${model2Type}) Loaded TensorFlow.js model from IndexedDB (${indexedDBURL}).`
        );
      },
      () => {
        getTfjsModel(model2URL).then(
          async (model: GraphModel) => {
            setTfModel(model);

            await model.save(indexedDBURL);

            console.log(
              `(${model2Type}) Saved TensorFlow.js model to IndexedDB (${indexedDBURL}).`
            );
          },
          () => {
            console.error(
              `(${model2Type}) Failed to load model from ${model2URL}.`
            );
          }
        );
      }
    );
  }

  useEffect(() => {
    if (model2Format == "onnx" && inferenceSession == null) {
      createInferenceSession(model2URL, sessionOptions).then(
        (session: InferenceSession | undefined) => {
          if (session) {
            setInferenceSession(session);
            console.log(`(${model2Type}) Done loading ONNX model.`);
          }
        }
      );
    }
  });

  return (
    <Container>
      <Row align="center">
        <Text h3>{title}</Text>
      </Row>
      <Row align="center">
        <Col css={{ textAlign: "center" }}>
          <ImageInputTitle />
        </Col>
        <Col span={1}></Col>
        <Col css={{ textAlign: "center" }}>
          <Text>Photo</Text>
        </Col>
        <Col span={1}></Col>
        <Col css={{ textAlign: "center" }}>
          <Text>Output</Text>
        </Col>
      </Row>
      <Row align="center">
        <Col css={{ textAlign: "center" }}>
          <ImageInput
            modelURL={model1URL}
            type={model1Type}
            format={model1Format}
            onRunInference={(result: boolean) => {
              const image = new Image();
              if (canvas1Ref.current) {
                image.src = canvas1Ref.current.toDataURL("image/jpeg", 1.0);
              }
              if (theme) {
                image.style.borderRadius = `${theme.radii.lg.value}`;
              }
              image.onload = () => {
                if (result == false) {
                  if (
                    model2Format == "onnx" &&
                    inferenceSession &&
                    canvas1Ref.current &&
                    canvas2Ref.current
                  ) {
                    drawOnnxPrediction(
                      inferenceSession,
                      canvas2Ref.current,
                      canvas1Ref.current.toDataURL("image/jpeg", 1.0)
                    ).then(() => {
                      setIsPredicted(true);
                      setIsLoading(result);
                    });
                  } else if (
                    model2Format == "tfjs" &&
                    tfModel &&
                    canvas1Ref.current &&
                    canvas2Ref.current
                  ) {
                    drawTfjsPrediction(
                      tfModel,
                      canvas2Ref.current,
                      canvas1Ref.current
                    ).then(() => {
                      setIsPredicted(true);
                      setIsLoading(result);
                    });
                  }
                }
              };
            }}
            canvasRef={canvas1Ref}
            labelRef={labelRef}
          />
        </Col>
        <Col span={1}>
          <Text css={{ fontSize: "3.5vw" }}>→</Text>
        </Col>
        <Col css={{ textAlign: "center" }}>
          <CanvasOutput
            type={model1Type}
            isLoading={isLoading}
            isPredicted={isPredicted}
            canvasRef={canvas1Ref}
          />
        </Col>
        <Col span={1}>
          <Text css={{ fontSize: "3.5vw" }}>→</Text>
        </Col>
        <Col css={{ textAlign: "center" }}>
          <CanvasOutput
            type={model2Type}
            isLoading={isLoading}
            isPredicted={isPredicted}
            canvasRef={canvas2Ref}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default Model2ModelCard;
