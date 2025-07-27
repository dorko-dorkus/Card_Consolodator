import React from 'react';
import renderer, { act } from 'react-test-renderer';

jest.mock('react-native', () => {
  const React = require('react');
  return {
    View: (props) => React.createElement('View', props, props.children),
    Text: (props) => React.createElement('Text', props, props.children),
    TextInput: (props) => React.createElement('TextInput', props),
    Button: (props) => React.createElement('Button', props),
    StyleSheet: { create: (styles) => styles },
    useColorScheme: () => 'light',
  };
});
import BankAccountScreen from '../BankAccountScreen';
import TopUpScreen from '../TopUpScreen';
import PurchaseScreen from '../PurchaseScreen';
import { linkBankAccount, transferFromBank, makePurchase } from '../api';

jest.mock('../api');

describe('banking flows', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  test('BankAccountScreen links account and shows message', async () => {
    linkBankAccount.mockResolvedValue({ message: 'bank account linked' });
    let tree;
    await act(async () => {
      tree = renderer.create(<BankAccountScreen />);
    });
    const root = tree.root;
    const input = root.findByProps({ placeholder: 'Bank token' });
    await act(async () => {
      input.props.onChangeText('tok_bank');
    });
    const button = root.findByProps({ title: 'Link Account' });
    await act(async () => {
      button.props.onPress();
    });
    expect(linkBankAccount).toHaveBeenCalledWith(1, 'tok_bank');
    const text = root.findAllByType(require('react-native').Text).find(t => t.props.children === 'bank account linked');
    expect(text).toBeTruthy();
  });

  test('TopUpScreen transfers funds and shows new balance', async () => {
    transferFromBank.mockResolvedValue({ new_balance: 15 });
    let tree;
    await act(async () => {
      tree = renderer.create(<TopUpScreen />);
    });
    const root = tree.root;
    const accInput = root.findByProps({ placeholder: 'Bank Account ID' });
    const amtInput = root.findByProps({ placeholder: 'Amount' });
    await act(async () => {
      accInput.props.onChangeText('1');
      amtInput.props.onChangeText('15');
    });
    const button = root.findByProps({ title: 'Transfer' });
    await act(async () => {
      button.props.onPress();
    });
    expect(transferFromBank).toHaveBeenCalledWith(1, '1', 15);
    const text = root.findAllByType(require('react-native').Text).find(t => t.props.children === 'New balance: $15');
    expect(text).toBeTruthy();
  });

  test('PurchaseScreen makes purchase and shows remaining balance', async () => {
    makePurchase.mockResolvedValue({ remaining_balance: 5 });
    let tree;
    await act(async () => {
      tree = renderer.create(<PurchaseScreen />);
    });
    const root = tree.root;
    const input = root.findByProps({ placeholder: 'Amount' });
    await act(async () => {
      input.props.onChangeText('5');
    });
    const button = root.findByProps({ title: 'Make Purchase' });
    await act(async () => {
      button.props.onPress();
    });
    expect(makePurchase).toHaveBeenCalledWith(1, 5);
    const text = root.findAllByType(require('react-native').Text).find(t => t.props.children === 'Remaining balance: $5');
    expect(text).toBeTruthy();
  });
});
