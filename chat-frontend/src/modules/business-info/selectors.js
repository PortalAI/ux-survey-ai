/* eslint-disable import/prefer-default-export */
import { createSelector } from '@reduxjs/toolkit';
import { initialState } from './slice';

const selectDomain = (state) => state['feature/business-info'] || initialState;
/**
 * Getting loader state to dashboard component
 */
export const selectLoader = createSelector(
  [selectDomain],
  (businessInfoState) => businessInfoState.loading
);
/**
 * Getting the business info state into the component
 */
export const selectSurveyInfo = createSelector(
  [selectDomain],
  (businessInfoState) => businessInfoState?.surveyInfo
);
/**
 * Getting the chat state state into the component
 */
export const selectChatState = createSelector(
  [selectDomain],
  (businessInfoState) => businessInfoState?.chatState
);
