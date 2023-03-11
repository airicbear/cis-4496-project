import { Card, FormElement, Input, useTheme, Text } from "@nextui-org/react";
import { ChangeEvent } from "react";

interface ImageInputProps {
  id: number;
}

const ImageInput = ({ id }: ImageInputProps) => {
  const { theme } = useTheme();

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const input = event.target as HTMLInputElement;
    const files = input.files;
    const label = document.getElementById(`label-file-upload-${id}`);
    const file = files[0];
    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        label.style.backgroundImage = `url(${reader.result})`;
        label.style.backgroundSize = "cover";
        label.style.backgroundRepeat = "no-repeat";
        label.textContent = "";
      },
      false
    );
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const setLabelTransparency = function (alpha: number) {
    const label = document.getElementById(`label-file-upload-${id}`);
    label.style.opacity = `${alpha}`;
  };

  const setLabelBackgroundColor = function (color: string) {
    const label = document.getElementById(`label-file-upload-${id}`);
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
    const files = event.dataTransfer.files;
    const label = document.getElementById(`label-file-upload-${id}`);
    const file = files[0];
    const reader = new FileReader();
    reader.addEventListener(
      "load",
      () => {
        label.style.backgroundImage = `url(${reader.result})`;
        label.style.backgroundSize = "cover";
        label.style.backgroundRepeat = "no-repeat";
        label.textContent = "";
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
        id={`input-file-upload-${id}`}
        accept=".jpg, .jpeg, .png"
        onChange={handleChange}
        style={{
          display: "none",
        }}
      ></Input>

      <label
        htmlFor={`input-file-upload-${id}`}
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
          style={{
            backgroundColor: `${theme.colors.neutralLight.value}`,
          }}
        >
          <Card.Body
            id={`label-file-upload-${id}`}
            style={{
              width: "256px",
              height: "256px",
              textAlign: "center",
              verticalAlign: "center",
            }}
          >
            <Text h3>Upload image</Text>
          </Card.Body>
        </Card>
      </label>
    </form>
  );
};

export default ImageInput;
