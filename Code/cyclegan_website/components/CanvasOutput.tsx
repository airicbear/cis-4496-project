import { Button, Container, Loading } from "@nextui-org/react";
import { RefObject, useState } from "react";

interface CanvasOutputProps {
  id: string;
  isLoading: boolean;
  isLoaded: boolean;
  canvasRef: RefObject<HTMLCanvasElement>;
}

const CanvasOutput = ({
  id,
  isLoading,
  isLoaded,
  canvasRef,
}: CanvasOutputProps) => {
  const [isMouseEnter, setIsMouseEnter] = useState(false);

  const getDisplay = () => {
    return isLoading ? "none" : "inline-flex";
  };

  const handleMouseEnter = () => {
    if (canvasRef.current) {
      canvasRef.current.style.opacity = "0.5";
    }
    setIsMouseEnter(true);
  };

  const handleMouseLeave = () => {
    if (canvasRef.current) {
      canvasRef.current.style.opacity = "1.0";
    }
    setIsMouseEnter(false);
  };

  const handleDownloadButtonClicked = () => {
    var link = document.createElement("a");
    link.download = "download.jpg";
    if (canvasRef.current) {
      link.href = canvasRef.current.toDataURL();
    }
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
        "@media (max-width: 955px)": {
          width: "171px",
        },
        "@media (max-width: 620px)": {
          width: "85px",
        },
      }}
    >
      {isLoading ? <Loading /> : <></>}
      {isLoaded && isMouseEnter && !isLoading ? (
        <Button
          auto
          css={{
            position: "absolute",
            bottom: "16px",
            left: "75px",
            zIndex: "5",
            "@media (max-width: 955px)": {
              left: "34px",
            },
            "@media (max-width: 620px)": {
              left: "2.5px",
              fontSize: "8px",
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
        id={id}
        className="image-display"
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
