import {useState ,memo, useCallback} from 'react'

function Call(){
  const [count,setCount] = useState(0);
  const resetCount = useCallback(() => setCount(0), [setCount])
  // const resetCount = () => {
  //   setCount(0);
  // }
  return (
    <div>
      <span>{count}</span>
      <button onClick={() => setCount(count +1)}>+1</button>
      <Foo resetCount={resetCount}></Foo>
    </div>
  )
}

const Foo = memo(function Foo(props) {
  console.log('Foo重新渲染')
  return <div>Foo组件
    <button onClick={props.resetCount}>resetCount</button>
  </div>
})

export default Call