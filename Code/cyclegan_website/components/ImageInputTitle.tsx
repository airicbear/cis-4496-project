import { Container, Link, Popover, Text } from "@nextui-org/react";
import { InfoIcon } from "./InfoIcon";

const ImageInputTitle = () => {
  return (
    <Container css={{ textAlign: "center", display: "flex", maxWidth: 110 }}>
      <Text
        css={{
          margin: "0 auto",
          display: "inline-block",
          position: "relative",
        }}
      >
        Input
      </Text>
      <Popover>
        <Popover.Trigger>
          <Link
            color="text"
            css={{
              margin: "0 auto",
              position: "relative",
            }}
          >
            <InfoIcon width={16} height={16} />
          </Link>
        </Popover.Trigger>
        <Popover.Content>
          <Text css={{ padding: "8px" }}>
            Supported image formats: JPG, PNG, WEBP, GIF, SVG
          </Text>
        </Popover.Content>
      </Popover>
    </Container>
  );
};
export default ImageInputTitle;
