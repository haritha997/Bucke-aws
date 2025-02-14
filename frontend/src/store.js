import { configureStore } from "@reduxjs/toolkit";
import fileReducer from "./fileslice.js";

const store = configureStore({
  reducer: { file: fileReducer },
});

export default store;
