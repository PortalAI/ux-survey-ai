/* eslint-disable no-param-reassign */
import { createSlice } from '@reduxjs/toolkit';
/**
 * Initial states of Dashboard function are defined here
 */
export const initialState = {
  loading: false,
  isInvalidHashId: false,
  summary: '',
};
/**
 * All actions related to presentation feature are defined here
 */
export const presentationSlice = createSlice({
  name: 'feature/presentation',
  initialState,
  reducers: {
    getPresentation(state) {
      state.loading = true;
    },
    getPresentationSucceeded(state) {
      state.loading = false;
      state.isInvalidHashId = false;
    },
    getPresentationFailed(state) {
      state.loading = false;
      state.isInvalidHashId = true;
    },
    getSummary(state) {
      state.loading = true;
    },
    getSummarySucceeded(state, action) {
      state.loading = false;
      state.summary = action?.payload;
    },
    getSummaryFailed(state) {
      state.loading = false;
    },
    resetSummary(state) {
      state.summary = '';
    },
  },
});
//
export const { actions: presentationActions } = presentationSlice;
