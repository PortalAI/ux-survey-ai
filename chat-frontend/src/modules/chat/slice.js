/* eslint-disable no-param-reassign */
import { createSlice } from '@reduxjs/toolkit';
/**
 * Initial states of Dashboard function are defined here
 */
export const initialState = {
  loading: false,
  isInvalidSurveyId: false,
};
/**
 * All actions related to dashboard feature are defined here
 */
export const chatSlice = createSlice({
  name: 'feature/chat',
  initialState,
  reducers: {
    validateSurveyLinkId: (state) => ({
      ...state,
      loading: true,
    }),
    validateSurveyLinkIdSucceeded: (state) => ({
      ...state,
      loading: false,
      isInvalidSurveyId: false,
    }),
    validateSurveyLinkIdFailed: (state) => ({
      ...state,
      loading: false,
      isInvalidSurveyId: true,
    }),
  },
});
//
export const { actions: chatActions } = chatSlice;
