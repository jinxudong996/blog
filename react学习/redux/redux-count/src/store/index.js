import { createStore,applyMiddleware } from "redux";
import Reducer from './reducers/counter.reducer'

// import thunk from './middleware/thunk'
import createSagaMidddleware from 'redux-saga';
import counterSaga from './sagas/counter.saga'

// 创建 sagaMiddleware
const sagaMiddleware = createSagaMidddleware();

export const store = createStore(Reducer, applyMiddleware(sagaMiddleware));

sagaMiddleware.run(counterSaga)