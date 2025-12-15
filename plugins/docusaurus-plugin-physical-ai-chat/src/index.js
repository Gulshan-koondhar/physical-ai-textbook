const path = require('path');

module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-physical-ai-chat',

    getClientModules() {
      return [path.resolve(__dirname, './components/ChatWidgetInjector')];
    },

    configureWebpack(config, isServer, utils) {
      return {
        resolve: {
          alias: {
            '@chat-widget': path.resolve(__dirname, './components'),
          },
        },
      };
    },
  };
};