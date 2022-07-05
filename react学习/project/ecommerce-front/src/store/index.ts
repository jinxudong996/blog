import { applyMiddleware, createStore,compose } from "redux";
import createRootReducer from "./reducer/index";
import {createBrowserHistory} from "history";
import { routerMiddleware } from "connected-react-router";

export const history = createBrowserHistory()

const store = createStore(
  createRootReducer(history),
  compose(
    applyMiddleware(
      routerMiddleware(history),
    ),
  )
)

export default store