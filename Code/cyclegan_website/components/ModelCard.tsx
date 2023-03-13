import { Col, Container, Row, Text } from "@nextui-org/react";
import ImageInput from "./ImageInput";

interface ModelCardProps {
  title: string;
  type: string;
}

const ModelCard = ({ title, type }: ModelCardProps) => {
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
        <Col>
          <ImageInput type={type} />
        </Col>
        <Col span={1}>
          <Text css={{ fontSize: "3.5vw" }}>→</Text>
        </Col>
        <Col>
          <canvas id={type}></canvas>
        </Col>
      </Row>
    </Container>
  );
};

export default ModelCard;
