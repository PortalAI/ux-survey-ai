/* eslint-disable import/no-cycle */
import { combineReducers, configureStore } from '@reduxjs/toolkit';
import createSagaMiddleware from 'redux-saga';
import rootSaga from 'root-saga';
import { businessInfoSlice } from 'modules/business-info/slice';
import { chatSlice } from 'modules/chat/slice';
import { presentationSlice } from 'modules/presentation/slice';

export const sagaMiddleware = createSagaMiddleware();
/**
 * Combine all the persist and non persist reducers
 */
const reducers = combineReducers({
  'feature/business-info': businessInfoSlice.reducer,
  'feature/chat': chatSlice.reducer,
  'feature/presentation': presentationSlice.reducer,
});
/**
 * Register all the slices into the main store with encryption
 */
const store = configureStore({
  reducer: reducers,
  middleware: () => [sagaMiddleware],
});
sagaMiddleware.run(rootSaga);
//
export default store;
