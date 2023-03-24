import { Loading } from "@nextui-org/react";

const CanvasOutput = ({ type, isLoading }) => {
  const getDisplay = () => {
    return isLoading ? "none" : "inline-flex";
  };

  return (
    <>
      {isLoading ? <Loading /> : <></>}
      <canvas
        id={type}
        width={256}
        height={256}
        style={{
          display: getDisplay(),
        }}
      />
    </>
  );
};

export default CanvasOutput;
