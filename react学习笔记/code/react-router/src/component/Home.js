function TabA(){

  function goTabA(){
    console.log('aaa')
  }
  function goTabB(){
    console.log('bbb')
  }

  return (
    <div>
      <button onClick={goTabA}>TabA</button>
      <button onClick={goTabB}>TabB</button>
    </div>
  )
  
}

export default TabA