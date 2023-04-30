import {
  Card,
  Checkbox,
  Col,
  Container,
  FormElement,
  Input,
  Radio,
  Row,
  Spacer,
  Text,
} from "@nextui-org/react";
import {
  add,
  browser,
  image,
  randomUniform,
  reverse,
  tensor1d,
} from "@tensorflow/tfjs";
import { NextPage } from "next";
import { ChangeEvent, useEffect, useRef, useState } from "react";
import AppHeader from "../../components/AppHeader";
import CanvasOutput from "../../components/CanvasOutput";
import ImageInputLabel from "../../components/ImageInputLabel";
import ImageInputTitle from "../../components/ImageInputTitle";
import { initializeLabel } from "../../utils/initializeLabel";
const AugmentImagePage: NextPage = () => {
  const labelRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const [rotation, setRotation] = useState("0");
  const [randomCrop, setRandomCrop] = useState("0");
  const [inputImage, setInputImage] = useState<HTMLImageElement | null>(null);
  const [flipSelection, setFlipSelection] = useState<string[]>([]);
  const [reader, setReader] = useState<FileReader | null>(null);

  useEffect(() => {
    if (!inputImage) {
      setInputImage(new Image());
    }
    if (!reader) {
      setReader(new FileReader());
    }
    if (reader) {
      reader.addEventListener(
        "load",
        () => {
          if (labelRef.current) {
            initializeLabel(labelRef.current, `url(${reader.result})`);
          }
          if (inputImage) {
            inputImage.src = reader.result as string;
          }
        },
        false
      );
    }
  });

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const file = files ? files[0] : null;

    if (inputImage) {
      inputImage.onload = () => {
        handleInputChange(rotation, randomCrop, flipSelection);
      };
    }

    if (reader && file) {
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (
    rotation: string,
    randomCrop: string,
    flipSelection: string[]
  ) => {
    if (canvasRef.current && inputImage) {
      const cropMargin = parseInt(randomCrop);
      let tensor = browser
        .fromPixels(inputImage)
        .toFloat()
        .mul(1 / 255)
        .resizeBilinear([256 + cropMargin, 256 + cropMargin]);

      // Random crop
      const boxInd = tensor1d([0], "int32");
      const yMin = randomUniform([], 0, cropMargin, "int32");
      const xMin = randomUniform([], 0, cropMargin, "int32");
      const yMax = add(yMin, 256);
      const xMax = add(xMin, 256);
      const cropped = image.cropAndResize(
        tensor.as4D(1, 256 + cropMargin, 256 + cropMargin, 3),
        [
          [
            yMin.dataSync()[0] / (256 + cropMargin),
            xMin.dataSync()[0] / (256 + cropMargin),
            yMax.dataSync()[0] / (256 + cropMargin),
            xMax.dataSync()[0] / (256 + cropMargin),
          ],
        ],
        boxInd,
        [256, 256]
      );

      // Rotate image
      let rotated = image.rotateWithOffset(
        cropped,
        Math.PI * (parseInt(rotation) / 2)
      );

      // Flip
      if (flipSelection.indexOf("left-right") > -1) {
        rotated = image.flipLeftRight(rotated);
      }
      if (flipSelection.indexOf("up-down") > -1) {
        rotated = reverse(rotated, [1]);
      }

      const augmentedImage = rotated.as3D(256, 256, 3);

      browser.toPixels(augmentedImage, canvasRef.current);
      setIsLoaded(true);
      setIsLoading(false);
    }
  };

  return (
    <Container sm>
      <AppHeader />
      <Container>
        <Row align="center">
          <Text h3>Augment Image</Text>
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
            <form style={{ textAlign: "center" }}>
              <Input
                type="file"
                id={"input-file-upload"}
                accept="image/*"
                onChange={handleChange}
                css={{
                  display: "none",
                }}
              ></Input>
              <ImageInputLabel
                htmlFor={"input-file-upload"}
                id={"label-input-rgb-distribution"}
                labelRef={labelRef}
              />
            </form>
          </Col>
          <Col span={1}>
            <Text css={{ fontSize: "3.5vw" }}>→</Text>
          </Col>
          <Col css={{ textAlign: "center" }}>
            <CanvasOutput
              id="output"
              isLoading={isLoading}
              isLoaded={isLoaded}
              canvasRef={canvasRef}
            />
          </Col>
        </Row>
        <Spacer y={2} />
        <Row gap={2}>
          <Col>
            <Card variant="bordered" css={{ minHeight: "250px" }}>
              <Card.Body css={{ textAlign: "center" }}>
                <Radio.Group
                  label="Rotation"
                  value={rotation}
                  onChange={(value: string) => {
                    setRotation(value);
                    if (isLoaded) {
                      handleInputChange(value, randomCrop, flipSelection);
                    }
                  }}
                >
                  <Radio value="0">0&deg;</Radio>
                  <Radio value="1">90&deg;</Radio>
                  <Radio value="2">180&deg;</Radio>
                  <Radio value="3">270&deg;</Radio>
                </Radio.Group>
              </Card.Body>
            </Card>
          </Col>
          <Col>
            <Card variant="bordered" css={{ minHeight: "250px" }}>
              <Card.Body css={{ textAlign: "center" }}>
                <Radio.Group
                  label="Random Crop"
                  value={randomCrop}
                  onChange={(value: string) => {
                    setRandomCrop(value);
                    if (isLoaded) {
                      handleInputChange(rotation, value, flipSelection);
                    }
                  }}
                >
                  <Radio value="0">+0px</Radio>
                  <Radio value="30">+33px</Radio>
                  <Radio value="44">+44px</Radio>
                </Radio.Group>
              </Card.Body>
            </Card>
          </Col>
          <Col>
            <Card variant="bordered" css={{ minHeight: "250px" }}>
              <Card.Body css={{ textAlign: "center" }}>
                <Checkbox.Group
                  label="Flip"
                  value={flipSelection}
                  onChange={(value: string[]) => {
                    setFlipSelection(value);
                    if (isLoaded) {
                      handleInputChange(rotation, randomCrop, value);
                    }
                  }}
                >
                  <Checkbox value="left-right">Left-right</Checkbox>
                  <Checkbox value="up-down">Up-down</Checkbox>
                </Checkbox.Group>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </Container>
  );
};

export default AugmentImagePage;
