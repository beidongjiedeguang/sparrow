const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/index.ts',
  devtool: 'source-map',
  mode: 'development',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist'),
  },
  externals: {
    // THREE: 'THREE',
    jquery: 'jQuery',
  },
  devServer: {
    // contentBase: path.join(__dirname, 'dist'),
    static: path.join(__dirname, 'dist'),
    port: 9090,
    open: true

  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {from: './src', to: './'},
      ],
    }),
  ],
};