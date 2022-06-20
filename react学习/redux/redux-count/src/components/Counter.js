import React from "react";
import {connect} from 'react-redux'

import { bindActionCreators } from 'redux';
import * as couterActions from '../store/actions/counter.actions';

function Counter({count,increment,decrement,increment_async}){
  return (
    <div>
      <button onClick={ () => increment_async(5)}>+</button>
      <span>{count}</span>
      <button onClick={() => decrement(5)}>-</button>
    </div>
  )
}

const mapStateToProps = state => ({
  count:state.count
})


// connect  第一个参数  就是state仓库  组件中的属性可以通过props.state拿到state
//          第二个参数  是一个函数 返回一个对象  该对象的属性都可以通过props拿到
const mapDispatchToProps = dispatch => bindActionCreators(couterActions, dispatch)

export default connect(mapStateToProps, mapDispatchToProps)(Counter);