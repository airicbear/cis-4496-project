import { Col, Container, Row, Text } from "@nextui-org/react";
import ImageInput from "./ImageInput";

interface ModelCardProps {
  title: string;
  type: string;
  modelURL: string;
  format: string;
}

const ModelCard = ({ title, type, modelURL, format }: ModelCardProps) => {
  return (
    <Container sm>
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
          <ImageInput modelURL={modelURL} type={type} format={format} />
        </Col>
        <Col span={1}>
          <Text css={{ fontSize: "3.5vw" }}>→</Text>
        </Col>
        <Col css={{ textAlign: "center" }}>
          <canvas id={type} width={256} height={256}></canvas>
        </Col>
      </Row>
    </Container>
  );
};

export default ModelCard;
