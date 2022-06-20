import React from 'react';
import ReactDOM from 'react-dom/client';
// import App from './App';

import {createStore} from 'redux';
import { Provider } from 'react-redux';

import Counter from './components/Counter.js'

const initialState = {
  count:0
}

function reducer(state = initialState,action){
  switch (action.type) {
    case 'increment':
      return {count: state.count + 1};
    case 'decrement':
      return {count: state.count - 1}
    default:
      return state;
  }
}

const store = createStore(reducer)


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider store={store}>
   <Counter/>
</Provider>
);

