const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/main.ts',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.py$/,
        use: 'raw-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.js', '.py'],
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'src/index.html',
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'node_modules/brython@3.11.0/brython.min.js',
          to: 'brython.min.js',
        },
        {
          from: 'node_modules/brython@3.11.0/brython_stdlib.js',
          to: 'brython_stdlib.js',
        },
      ],
    }),
  ],
  devServer: {
    static: './dist',
  },
  mode: 'production',
};
