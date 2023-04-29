import { Card, Link, Row, useTheme } from "@nextui-org/react";

interface CardLinkProps {
  img: string;
  title: string;
  url: string;
  fontSize?: string;
  fontSizeSmall?: string;
}

const CardLink = ({
  img,
  title,
  url,
  fontSize = "16px",
  fontSizeSmall = "12px",
}: CardLinkProps) => {
  const { theme } = useTheme();

  return (
    <Card variant="bordered">
      <Card.Body css={{ p: 0 }}>
        <Card.Image
          src={img}
          objectFit="cover"
          width="100%"
          height={168}
          alt={title}
        />
      </Card.Body>
      <Card.Footer
        isBlurred
        css={{
          position: "absolute",
          bgBlur: `${theme?.colors.background.value}66`,
          borderTop: "$borderWeights$light solid rgba(255, 255, 255, 0.2)",
          bottom: 0,
          zIndex: 1,
        }}
      >
        <Row wrap="wrap" justify="space-between" align="center">
          <Link
            href={url}
            block
            color="text"
            css={{
              fontWeight: "bold",
              fontSize: fontSize,
              "@media (max-width: 955px)": {
                fontSize: fontSizeSmall,
              },
            }}
          >
            {title}
          </Link>
        </Row>
      </Card.Footer>
    </Card>
  );
};

export default CardLink;
