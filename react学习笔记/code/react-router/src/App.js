import Home from "./component/Home"
import { BrowserRouter, Route, Routes  } from 'react-router-dom';
import {renderRoutes} from "react-router-config"
import TabA from "./component/TabA";
import TabB from "./component/TabB";
import {Suspense} from "react"


let RouteList = [
  {
      name: '首页',
      path: '/router/home',  
      exact:true,
      component:TabA
  },
  {
      name: '列表页',
      path: '/router/list',  
      component:TabB
  },
]

function App() {
  return (
    <div className="App">
     {/* <Home></Home> */}
     
     <BrowserRouter>
        <Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path='/TabA' exact element={<TabA></TabA>}></Route>
            <Route path='/TabB' exact element={<TabB></TabB>}></Route>
            <Route path='/' exact element={<Home></Home>}></Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </div>
  );
}

export default App;
