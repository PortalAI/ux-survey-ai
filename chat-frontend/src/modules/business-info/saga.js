/* eslint-disable import/no-cycle */
import { call, put, takeLatest } from 'redux-saga/effects';
import request from 'modules/common/utils/request';
import { businessInfoActions } from './slice';
import API from './constants';

/**
 * create survey generator function to create business survey
 * @param {*} param0
 */
export function* createSurveyGenerator({ payload }) {
  try {
    const response = yield call(request, API.POST_SURVEY, payload);
    yield put(businessInfoActions.createSurveySucceeded(response));
  } catch (error) {
    yield put(businessInfoActions.createSurveyFailed(error?.message));
  }
}
export function* businessInfoSaga() {
  yield takeLatest(businessInfoActions.createSurvey.type, createSurveyGenerator);
}
//
export default businessInfoSaga;
