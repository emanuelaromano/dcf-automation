import { configureStore } from "@reduxjs/toolkit";
import processingReducer from "./slices/processing";

const store = configureStore({
  reducer: {
    processing: processingReducer,
  },
});

export default store;
