/* eslint-disable import/prefer-default-export */
import { createSelector } from '@reduxjs/toolkit';
import { initialState } from './slice';

const selectDomain = (state) => state['feature/presentation'] || initialState;
/**
 * Getting loader state to dashboard component
 */
export const selectLoader = createSelector(
  [selectDomain],
  (presentationState) => presentationState.loading
);
/**
 * Getting the is invalid hash state into the component
 */
export const selectIsInvalidHashId = createSelector(
  [selectDomain],
  (presentationState) => presentationState?.isInvalidHashId
);
/**
 * Getting the summary state into the component
 */
export const selectSummary = createSelector(
  [selectDomain],
  (presentationState) => presentationState?.summary
);
