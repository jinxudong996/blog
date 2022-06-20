import React from 'react';
import ReactDOM from 'react-dom/client';
// import App from './App';

import { Provider } from 'react-redux';

import Counter from './components/Counter.js'
import { store } from './store'; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider store={store}>
   <Counter/>
</Provider>
);

