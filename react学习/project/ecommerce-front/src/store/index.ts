import { applyMiddleware, createStore,compose } from "redux";
import createRootReducer from "./reducer/index";
import {createHashHistory} from "history";
import { routerMiddleware } from "connected-react-router";

export const history = createHashHistory()

const store = createStore(
  createRootReducer(history),
  // compose(
    applyMiddleware(routerMiddleware(history)),
  // )
)

export default store