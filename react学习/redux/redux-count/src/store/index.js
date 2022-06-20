import { createStore,applyMiddleware } from "redux";
import Reducer from './reducers/counter.reducer'

import thunk from './middleware/thunk'

export const store = createStore(Reducer,applyMiddleware(thunk))