import { createContext,useContext } from "react";

const countContext = createContext();


function Context(){
  return <countContext.Provider value = {100}>
    <Foo></Foo>
  </countContext.Provider>
}

function Foo(){
  const value = useContext(countContext)
  return <div>{value}</div>
  // return <countContext.Consumer>
  //   {
  //     value =>{
  //       return <div>{value}</div>
  //     }
  //   }
  // </countContext.Consumer>
}

export default Context