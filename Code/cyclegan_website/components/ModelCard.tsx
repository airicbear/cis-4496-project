import { Col, Container, Row, Text } from "@nextui-org/react";
import { useState } from "react";
import CanvasOutput from "./CanvasOutput";
import ImageInput from "./ImageInput";

interface ModelCardProps {
  title: string;
  type: string;
  modelURL: string;
  format: string;
}

const ModelCard = ({ title, type, modelURL, format }: ModelCardProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isPredicted, setIsPredicted] = useState(false);

  return (
    <Container>
      <Row align="center">
        <Text h3>{title}</Text>
      </Row>
      <Row align="center">
        <Col css={{ textAlign: "center" }}>
          <Text>Input</Text>
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
              setIsPredicted(true);
              setIsLoading(result);
            }}
          />
        </Col>
        <Col span={1}>
          <Text css={{ fontSize: "3.5vw" }}>→</Text>
        </Col>
        <Col css={{ textAlign: "center" }}>
          <CanvasOutput
            type={type}
            isLoading={isLoading}
            isPredicted={isPredicted}
          />
        </Col>
      </Row>
    </Container>
  );
};

export default ModelCard;
