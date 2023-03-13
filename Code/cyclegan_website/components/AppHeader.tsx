import {
  Col,
  Container,
  Link,
  Row,
  Switch,
  Text,
  useTheme,
} from "@nextui-org/react";
import { useTheme as useNextTheme } from "next-themes";
import { GitHubIcon } from "./GitHubIcon";
import { MoonIcon } from "./MoonIcon";
import { SunIcon } from "./SunIcon";

const AppHeader = () => {
  const { setTheme } = useNextTheme();
  const { isDark, type } = useTheme();

  const handleThemeToggle = function (event) {
    setTheme(event.target.checked ? "dark" : "light");
  };

  return (
    <Container sm>
      <Row align="center">
        <Col>
          <Text
            h1
            css={{
              "@media (max-width: 620px)": {
                fontSize: "24px",
              },
            }}
          >
            <Link color="text" href="/">
              Photo ⇆ Painting
            </Link>
          </Text>
        </Col>
        <Col span={3}>
          <Row align="center">
            <Col style={{ padding: "16px" }}>
              <Switch
                checked={isDark}
                onChange={handleThemeToggle}
                iconOn={<SunIcon filled />}
                iconOff={<MoonIcon filled />}
              />
            </Col>
            <Col>
              <Link
                href="https://github.com/airicbear/cis-4496-project"
                color="text"
              >
                <GitHubIcon />
              </Link>
            </Col>
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default AppHeader;
