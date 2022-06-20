import { createStore } from "redux";
import Reducer from './reducers/counter.reducer'

export const store = createStore(Reducer)