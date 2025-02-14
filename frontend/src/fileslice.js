import { createSlice } from "@reduxjs/toolkit";

const bucketSlice = createSlice({
  name: "bucket",
  initialState: { name: "" },
  reducers: {
    setBucketName: (state, action) => {
      state.name = action.payload;
    },
  },
});

export const { setBucketName } = bucketSlice.actions;
export default bucketSlice.reducer;