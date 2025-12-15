const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/chatWidgetLoader.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'chat-widget.js',
    library: 'PhysicalAIChatWidget',
    libraryTarget: 'window',
    libraryExport: 'default'
  },
  resolve: {
    extensions: ['.js', '.jsx', '.json']
  },
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
      filename: 'index.html'
    })
  ],
  // Remove externals to bundle React with the widget
  externals: {}
};