import { Card, Text, useTheme } from "@nextui-org/react";
import { DragEvent } from "react";
import { initializeLabel } from "../utils/initializeLabel";

const ImageInputLabel = ({
  htmlFor,
  onFileUpload = (reader: FileReader) => {},
  id,
  labelRef,
  imageOnLoad = (image) => {},
}) => {
  const { theme } = useTheme();

  const handleDrop = function (event: DragEvent) {
    event.stopPropagation();
    event.preventDefault();

    const image = new Image();

    const files = event.dataTransfer.files;
    const file = files[0];

    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        initializeLabel(labelRef.current, `url(${reader.result})`);
        image.src = reader.result as string;
        onFileUpload(reader);
      },
      false
    );
    image.onload = () => imageOnLoad(image);
    if (file) {
      reader.readAsDataURL(file);
    }

    setLabelTransparency(1.0);
    setLabelBackgroundColor(`${theme.colors.neutralLight.value}`);
  };

  const setLabelTransparency = function (alpha: number) {
    labelRef.current.style.opacity = `${alpha}`;
  };

  const setLabelBackgroundColor = function (color: string) {
    labelRef.current.style.backgroundColor = `${color}`;
  };

  const handleDragOver = function (event: DragEvent) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
    setLabelTransparency(0.5);
    setLabelBackgroundColor(`${theme.colors.neutralBorderHover.value}`);
  };

  const handleDragLeave = function (event: DragEvent) {
    event.stopPropagation();
    event.preventDefault();
    setLabelTransparency(1.0);
    setLabelBackgroundColor(`${theme.colors.neutralLight.value}`);
  };
  return (
    <label
      htmlFor={htmlFor}
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
          id={id}
          ref={labelRef}
          css={{
            width: "256px",
            height: "256px",
            textAlign: "center",
            verticalAlign: "center",
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            flexDirection: "column",
            "@media (max-width: 955px)": {
              width: "171px",
              height: "171px",
              fontSize: "16px",
            },
            "@media (max-width: 620px)": {
              width: "85px",
              height: "85px",
            },
          }}
        >
          <Text
            h3
            css={{
              "@media (max-width: 955px)": {
                fontSize: "16px",
              },
              "@media (max-width: 620px)": {
                fontSize: "8px",
              },
            }}
          >
            Upload image
          </Text>
          <Text
            css={{
              "@media (max-width: 955px)": {
                fontSize: "12px",
              },
              "@media (max-width: 620px)": {
                fontSize: "6px",
              },
            }}
          >
            (Click or Drag/Drop)
          </Text>
        </Card.Body>
      </Card>
    </label>
  );
};

export default ImageInputLabel;
