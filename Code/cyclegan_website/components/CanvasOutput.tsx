import { Button, Container, Loading } from "@nextui-org/react";
import { useState } from "react";

const CanvasOutput = ({ type, isLoading, isPredicted, canvasRef }) => {
  const [isMouseEnter, setIsMouseEnter] = useState(false);

  const getDisplay = () => {
    return isLoading ? "none" : "inline-flex";
  };

  const handleMouseEnter = () => {
    canvasRef.current.style.opacity = "0.5";
    setIsMouseEnter(true);
  };

  const handleMouseLeave = () => {
    canvasRef.current.style.opacity = "1.0";
    setIsMouseEnter(false);
  };

  const handleDownloadButtonClicked = () => {
    var link = document.createElement("a");
    link.download = "download.jpg";
    link.href = canvasRef.current.toDataURL();
    link.click();
  };

  return (
    <Container
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      css={{
        position: "relative",
        width: "256px",
        padding: "0",
        "@media (max-width: 620px)": {
          width: "128px",
          backgroundSize: "128px 128px",
        },
      }}
    >
      {isLoading ? <Loading /> : <></>}
      {isPredicted && isMouseEnter && !isLoading ? (
        <Button
          auto
          css={{
            position: "absolute",
            bottom: "16px",
            left: "75px",
            zIndex: "5",
            "@media (max-width: 620px)": {
              left: "11px",
            },
          }}
          onClick={handleDownloadButtonClicked}
        >
          Download
        </Button>
      ) : (
        <></>
      )}
      <canvas
        ref={canvasRef}
        id={type}
        width={256}
        height={256}
        style={{
          display: getDisplay(),
        }}
      />
    </Container>
  );
};

export default CanvasOutput;
