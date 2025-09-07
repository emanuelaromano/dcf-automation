import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  bannerStatus: { message: null, type: null },
  processingStatus: "idle", // "idle", "generating", "cancelling", "cancelled"
  abortController: null,
};

const processingSlice = createSlice({
  name: "processing",
  initialState,
  reducers: {
    setBannerStatus: (state, action) => {
      state.bannerStatus = action.payload;
    },
    setProcessingStatus: (state, action) => {
      state.processingStatus = action.payload;
    },
    setAbortController: (state, action) => {
      state.abortController = action.payload;
    },
    clearAbortController: (state) => {
      state.abortController = null;
    },
  },
});

export const {
  setBannerStatus,
  setProcessingStatus,
  setAbortController,
  clearAbortController,
} = processingSlice.actions;

export default processingSlice.reducer;

export const setBannerStatusThunk = (status) => {
  return async (dispatch) => {
    dispatch(setBannerStatus(status));
    setTimeout(() => {
      dispatch(setBannerStatus(null));
    }, 3000);
  };
};
