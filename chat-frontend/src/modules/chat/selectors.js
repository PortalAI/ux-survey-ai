/* eslint-disable import/prefer-default-export */
import { createSelector } from '@reduxjs/toolkit';
import { initialState } from './slice';

const selectDomain = (state) => state['feature/chat'] || initialState;
/**
 * Getting loader state to chat component
 */
export const selectLoader = createSelector([selectDomain], (chatState) => chatState.loading);
/**
 * Selector for isInvalidSurveyId state
 */
export const selectIsInvalidSurveyId = createSelector(
  [selectDomain],
  (chatState) => chatState.isInvalidSurveyId
);
