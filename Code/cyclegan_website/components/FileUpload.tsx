import { Col, Container, Row, Spacer, Text } from "@nextui-org/react";
import ImageInput from "./ImageInput";

const FileUpload = () => {
  return (
    <Container sm>
      <Row align="center">
        <Col css={{ textAlign: "center" }}>
          <Text>Photo</Text>
        </Col>
        <Col span={1}></Col>
        <Col css={{ textAlign: "center" }}>
          <Text>Painting</Text>
        </Col>
      </Row>
      <Spacer y={0.5} />
      <Row align="center">
        <Col css={{ textAlign: "center" }}>
          <ImageInput id={1} />
        </Col>
        <Col span={1} css={{ textAlign: "center" }}>
          <Text css={{ fontSize: "3.5vw" }}>⇆</Text>
        </Col>
        <Col css={{ textAlign: "center" }}>
          <ImageInput id={2} />
        </Col>
      </Row>
    </Container>
  );
};

export default FileUpload;
