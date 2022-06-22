import {useState} from 'react'
import Usereducer from './components/Usereducer.js'
import Context from './components/context'

function App() {
  
  const [count ,setCount] = useState(0);
  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(count + 1)}>点击</button>
      <Usereducer></Usereducer>
      <Context></Context>
    </div>
  );
}

export default App;
