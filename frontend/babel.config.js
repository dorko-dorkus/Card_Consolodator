module.exports = {
  presets: [
    'module:metro-react-native-babel-preset',
    ["@babel/preset-env", { targets: { node: 'current' } }],
    '@babel/preset-react',
  ],
  plugins: ['expo-router/babel'],
};
