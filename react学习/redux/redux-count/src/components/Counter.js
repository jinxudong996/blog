import React from "react";
import {connect} from 'react-redux'

const increment = {type:'increment'}
const decrement = {type:'decrement'}

function Counter({count,dispatch}){
  return (
    <div>
      <button onClick={() => dispatch(increment)}>+</button>
      <span>{count}</span>
      <button onClick={() => dispatch(decrement)}>-</button>
    </div>
  )
}

const mapStateToProps = state => ({
  count:state.count
})



export default connect(mapStateToProps)(Counter)