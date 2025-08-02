const React = require("../../frontend/node_modules/react");
const renderer = require("../../frontend/node_modules/react-test-renderer");
const { act } = renderer;
jest.mock("react", () => require("../../frontend/node_modules/react"));

jest.mock("react-native", () => {
  const React = require("react");
  return {
    View: (props) => React.createElement("View", props, props.children),
    Text: (props) => React.createElement("Text", props, props.children),
    TextInput: (props) => React.createElement("TextInput", props),
    Button: (props) => React.createElement("Button", props),
    ActivityIndicator: (props) =>
      React.createElement("ActivityIndicator", props),
    StyleSheet: { create: (styles) => styles },
  };
});

import LoginScreen from "../LoginScreen";
import BankLinkScreen from "../BankLinkScreen";
import { loginUser, sessionInfo, linkBankAccount } from "../api";

jest.mock("../api");

describe("mobile screens", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test("LoginScreen displays error on failed login", async () => {
    loginUser.mockResolvedValue({ error: "Invalid" });
    sessionInfo.mockResolvedValue({});
    let tree;
    const navigation = { replace: jest.fn() };
    await act(async () => {
      tree = renderer.create(React.createElement(LoginScreen, { navigation }));
    });
    const root = tree.root;
    const emailInput = root.findByProps({ placeholder: "Email" });
    const passwordInput = root.findByProps({ placeholder: "Password" });
    await act(async () => {
      emailInput.props.onChangeText("user@example.com");
      passwordInput.props.onChangeText("secret");
    });
    const button = root.findByProps({ title: "Login" });
    await act(async () => {
      button.props.onPress();
    });
    expect(loginUser).toHaveBeenCalledWith("user@example.com", "secret");
    const text = root
      .findAllByType(require("react-native").Text)
      .find((t) => t.props.children === "Invalid");
    expect(text).toBeTruthy();
  });

  test("BankLinkScreen warns when token missing", async () => {
    sessionInfo.mockResolvedValue({ authenticated: true, user_id: 1 });
    let tree;
    await act(async () => {
      tree = renderer.create(React.createElement(BankLinkScreen));
    });
    const root = tree.root;
    const button = root.findByProps({ title: "Link" });
    await act(async () => {
      button.props.onPress();
    });
    const text = root
      .findAllByType(require("react-native").Text)
      .find((t) => t.props.children === "Enter bank token");
    expect(text).toBeTruthy();
    expect(linkBankAccount).not.toHaveBeenCalled();
  });
});
