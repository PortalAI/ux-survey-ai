/* eslint-disable import/no-cycle */
import { call, put, takeLatest } from 'redux-saga/effects';
import request from 'modules/common/utils/request';
import { chatActions } from './slice';
import API from './constants';
/**
 * Generator function for create survey session
 * @param {Object} payload
 */
export function* validateSurveyLinkGenerator({ payload }) {
  try {
    const response = yield call(request, API.GET_VALIDATE_SURVEY_ID, payload);
    yield put(chatActions.validateSurveyLinkIdSucceeded(response));
  } catch (error) {
    yield put(chatActions.validateSurveyLinkIdFailed(error?.message));
  }
}
/**
 * Redux saga that triggers above generated functions
 */
export function* chatSaga() {
  yield takeLatest(chatActions.validateSurveyLinkId.type, validateSurveyLinkGenerator);
}
//
export default chatSaga;
