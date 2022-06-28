import { combineReducers } from "redux";
import testReducer from "./test.reducer";

const rootReducer= combineReducers({
  test:testReducer
})

export default rootReducer