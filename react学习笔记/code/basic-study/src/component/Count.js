
import React, { useEffect, useRef, useState } from 'react';

class Count extends React.Component {
  constructor(props){
    super(props);
    this.state = {num:0};
  }
  handleClickAdd = (e,num) =>{
    this.setState({
      num:this.state.num + 1
    })
  }
  handleClickReduce = () => {
    console.log(this)
    this.setState({
      num:this.state.num - 1
    },(e) => {
      console.log(this.state.num)
      console.log('state更改了');
    })
  }
  render(){
    return (
      <div>
        <span a-data={this.props.value}>{this.state.num}</span>
        <button onClick={this.handleClickAdd.bind(this,'456')}>bunmer++</button>
        <button onClick={this.handleClickReduce}>bunmer--</button>
      </div>
    )
  }
}

export default Count