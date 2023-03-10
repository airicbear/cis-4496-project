import { FormElement, Input, useTheme } from "@nextui-org/react";
import { ChangeEvent } from "react";

const FileUpload = () => {
  const { theme } = useTheme();

  const handleChange = function (event: ChangeEvent<FormElement>) {
    event.stopPropagation();
    event.preventDefault();

    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      alert(`${input.files[0]}`);
    }
  };

  const handleDragOver = function (event: {
    stopPropagation: () => void;
    preventDefault: () => void;
    dataTransfer: { dropEffect: string };
  }) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
  };

  const handleDrop = function (event: {
    stopPropagation: () => void;
    preventDefault: () => void;
    dataTransfer: { files: any };
  }) {
    event.stopPropagation();
    event.preventDefault();
    const files = event.dataTransfer.files;
    const output = document.getElementById("output");
    for (let i = 0; i < files.length; i++) {
      const li = document.createElement("li");
      const file = files[i];
      const name = file.name ? file.name : "NOT SUPPORTED";
      const type = file.type ? file.type : "NOT SUPPORTED";
      const size = file.size ? file.size : "NOT SUPPORTED";
      li.textContent = `name: ${name}, type: ${type}, size: ${size}`;
      output.appendChild(li);
    }
  };

  return (
    <center>
      <form
        style={{
          height: "256px",
          width: "256px",
          maxWidth: "100%",
          textAlign: "center",
          position: "relative",
        }}
      >
        <Input
          type="file"
          id="input-file-upload"
          accept=".jpg, .jpeg, .png"
          onChange={handleChange}
          style={{
            display: "none",
          }}
        ></Input>
        <label
          htmlFor="input-file-upload"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          style={{
            boxShadow: `${theme.shadows.lg.value}`,
            height: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderWidth: `${theme.borderWeights.bold.value}`,
            borderStyle: "dashed",
            borderColor: `${theme.colors.border.value}`,
            borderRadius: `${theme.radii.lg.value}`,
            backgroundColor: `${theme.colors.border.value}`,
            fontSize: `${theme.fontSizes.lg.value}`,
            fontWeight: `${theme.fontWeights.bold.value}`,
          }}
        >
          Upload 256x256 Image
        </label>
      </form>
      <br />
      <ul id="output"></ul>
    </center>
  );
};

export default FileUpload;
