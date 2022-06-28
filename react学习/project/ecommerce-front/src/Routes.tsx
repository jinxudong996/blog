import React from 'react'
import {HashRouter,Route,Switch} from "react-router-dom"
import Home from './components/core/Home'
import Shop from './components/core/Shop'

const Routes = () => {
  return <HashRouter>
    <Switch>
      <Route path="/home" component={Home}></Route>
      <Route path="/shop" component={Shop}></Route>
    </Switch>
  </HashRouter>
}

export default Routes