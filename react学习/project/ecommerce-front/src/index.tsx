import React from 'react';
import ReactDOM from 'react-dom/client';
import Routes from './Routes';
import {Provider} from 'react-redux';
import { ConnectedRouter } from 'connected-react-router';

import store from './store/index'
import {history} from './store'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <Provider store={store}>
    <Routes />
    
  </Provider>
);
