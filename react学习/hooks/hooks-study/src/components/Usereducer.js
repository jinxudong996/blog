import { useReducer } from "react";

function reducer(state,action){
  switch(action.type){
    case 'increment':
      return state + 1;
    case 'decrement':
      return state - 1;
    default:
      return state
  }
}

function Usereducer(){
  const [count,dispath] = useReducer(reducer,0);
  return <div>
    <button onClick={() => dispath({type:'increment'})}>加</button>
    <span>{count}</span>
    <button onClick={() => dispath({type:'decrement'})}>减</button>
  </div>
}

export default Usereducer