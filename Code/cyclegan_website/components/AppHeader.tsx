import { Link, Text } from "@nextui-org/react";

const AppHeader = () => {
  return (
    <center>
      <Text h1>
        <Link color="text" href="/">
          Photo → Painting
        </Link>
      </Text>
    </center>
  );
};

export default AppHeader;
