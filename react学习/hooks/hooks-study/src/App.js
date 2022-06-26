import {useState} from 'react'
import Usereducer from './components/Usereducer.js'
import Context from './components/context'
import Call from './components/useCall'
import CustomHooks from './components/hooks'

function App() {
  
  const [count ,setCount] = useState(0);
  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(count + 1)}>点击</button>
      <Usereducer></Usereducer>
      <Context></Context>
      <span>#######################################</span>
      <Call></Call>
      <span>#################自定义hooks######################</span>
      <CustomHooks></CustomHooks>
    </div>
  );
}

export default App;
