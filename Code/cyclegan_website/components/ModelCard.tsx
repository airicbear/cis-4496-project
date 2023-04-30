import { Col, Container, Row, Text } from "@nextui-org/react";
import { useRef, useState } from "react";
import CanvasOutput from "./CanvasOutput";
import ImageInput from "./ImageInput";
import ImageInputTitle from "./ImageInputTitle";

interface ModelCardProps {
  title: string;
  type: string;
  modelURL: string;
  format: string;
}

const ModelCard = ({ title, type, modelURL, format }: ModelCardProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const labelRef = useRef<HTMLDivElement>(null);

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
          <Text>Output</Text>
        </Col>
      </Row>
      <Row align="center">
        <Col css={{ textAlign: "center" }}>
          <ImageInput
            modelURL={modelURL}
            type={type}
            format={format}
            onRunInference={(result: boolean) => {
              setIsLoaded(true);
              setIsLoading(result);
            }}
            canvasRef={canvasRef}
            labelRef={labelRef}
          />
        </Col>
        <Col span={1}>
          <Text css={{ fontSize: "3.5vw" }}>→</Text>
        </Col>
        <Col css={{ textAlign: "center" }}>
          <CanvasOutput
            id={type}
            isLoading={isLoading}
            isLoaded={isLoaded}
            canvasRef={canvasRef}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default ModelCard;
