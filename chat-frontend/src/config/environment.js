/**
 * Define all the .env file related keys
 */
const ENVIRONMENT = {
  BACKEND_API: process.env?.REACT_APP_BACKEND_API || 'https://survey-bot.portal-ai-dev.com',
  APP_NAME: process.env?.REACT_APP_APP_NAME  || 'Survey Chat',
  WEB_SOCKET_URL: process.env?.REACT_APP_WEBSOCKET_URL || 'wss://survey-bot.portal-ai-dev.com/chat',
};
//
export default ENVIRONMENT;
