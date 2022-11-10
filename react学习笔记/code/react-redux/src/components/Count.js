import {Component} from 'react'

import {connect} from 'react-redux'

const increment = {type:'increment'}
const decrement = {type:'decrement'}

class Count extends Component{
  constructor(props,a,b,c){
    super(props)
    // this.state = {count:0}
    this.count = props.count
    this.increment = props.increment
    this.decrement = props.decrement
    
    this.increase = this.increase.bind(this)
    this.decrease = this.decrease.bind(this)
  }
  render(e){
    return (
      <div>
        <div>当前的数字:{this.props.count}</div>
        <button onClick={this.increment}>加一</button>
        <button onClick={this.decrement}>减一</button>
      </div>
    )
  }
  increase(){
    this.setState({
      count:this.state.count + 1
    })
  }
  decrease(){
    this.setState({
      count:this.state.count - 1
    })
  }
}

const mapStateToProps = state => ({
  count:state.count
})

const mapDispatchToProps = dispatch => ({
  increment() {
    dispatch(increment)
  },
  decrement() {
    dispatch(decrement)
  }
})

// connect  第一个参数  就是state仓库  组件中的属性可以通过props.state拿到state
//          第二个参数  是一个函数 返回一个对象  该对象的属性都可以通过props拿到
export default connect(mapStateToProps,mapDispatchToProps)(Count)

