/**
 * Presentation feature related request structures are defined here
 */
const API = {
  GET_PRESENTATION: {
    path: '/presentation/:hashId',
    method: 'GET',
  },
  GET_SUMMARY: {
    path: '/summarize_survey/:hashId',
    method: 'GET',
  },
};
//
export default API;
