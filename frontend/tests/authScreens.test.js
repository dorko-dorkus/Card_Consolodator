import React from "react";
import renderer, { act } from "react-test-renderer";

jest.mock("react-native", () => {
  const React = require("react");
  return {
    View: (props) => React.createElement("View", props, props.children),
    Text: (props) => React.createElement("Text", props, props.children),
    TextInput: (props) => React.createElement("TextInput", props),
    Button: (props) => React.createElement("Button", props),
    TouchableOpacity: (props) =>
      React.createElement("TouchableOpacity", props, props.children),
    StyleSheet: { create: (styles) => styles },
    useColorScheme: () => "light",
  };
});

jest.mock("../SecureStore", () => ({
  getItem: jest.fn(),
  saveItem: jest.fn(),
  deleteItem: jest.fn(),
}));

import LoginScreen from "../LoginScreen";
import RegisterScreen from "../RegisterScreen";
import { AuthContext } from "../AuthContext";

describe("auth screens", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test("LoginScreen shows error message on failed login", async () => {
    const login = jest.fn().mockResolvedValue({ error: "invalid credentials" });
    let tree;
    await act(async () => {
      tree = renderer.create(
        <AuthContext.Provider value={{ login }}>
          <LoginScreen navigation={{ navigate: jest.fn() }} />
        </AuthContext.Provider>,
      );
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
    expect(login).toHaveBeenCalledWith("user@example.com", "secret");
    const text = root
      .findAllByType(require("react-native").Text)
      .find((t) => t.props.children === "invalid credentials");
    expect(text).toBeTruthy();
  });

  test("RegisterScreen shows error message on failed register", async () => {
    const register = jest.fn().mockResolvedValue({ error: "email taken" });
    let tree;
    await act(async () => {
      tree = renderer.create(
        <AuthContext.Provider value={{ register }}>
          <RegisterScreen navigation={{ navigate: jest.fn() }} />
        </AuthContext.Provider>,
      );
    });
    const root = tree.root;
    const nameInput = root.findByProps({ placeholder: "Name" });
    const emailInput = root.findByProps({ placeholder: "Email" });
    const passwordInput = root.findByProps({ placeholder: "Password" });
    await act(async () => {
      nameInput.props.onChangeText("User");
      emailInput.props.onChangeText("user@example.com");
      passwordInput.props.onChangeText("secret");
    });
    const button = root.findByProps({ title: "Register" });
    await act(async () => {
      button.props.onPress();
    });
    expect(register).toHaveBeenCalledWith("User", "user@example.com", "secret");
    const text = root
      .findAllByType(require("react-native").Text)
      .find((t) => t.props.children === "email taken");
    expect(text).toBeTruthy();
  });
});
