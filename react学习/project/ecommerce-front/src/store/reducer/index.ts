import { connectRouter } from "connected-react-router";
import { combineReducers } from "redux";
import testReducer from "./test.reducer";
import {History} from 'history'

const createRootReducer =  (history:History) =>
  combineReducers({
    test:testReducer,
    router:connectRouter(history)
  })

export default createRootReducer