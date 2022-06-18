##### 简介

`React`是一个用于构建用户界面的`JavaScript`库，他只是负责应用的视图层，帮助开发人员构建快速且交互式的web应用程序。以往传统的构建web应用，都是由`html+css+JavaScript`来构建的，使用了`React`以后，构建用户界面都是由`JavaScript`来完成的。也就是`all in JavaScript`。详细可以查看中文的react[文档](https://react.docschina.org/)

##### jsx

在`React`中使用jsx语法来描述用户界面，它是一种JavaScript的扩展，也就是充当html的角色，实际上就是一种语法糖，让开发人员更加舒服的构建用户界面。接下来详细的介绍下它的语法：

###### 在jsx中使用表达式

```javascript
const user = {
	firstName:'nick',
	lastName:'jin'
}
function formatName(user){
	return user.firstName + ' ' + user.lastName;
}

const element = <h1>hello,{formatName(user)}</h1>
```

jsx本身就是一个表达式，将他赋值给变量，当做参数传入，作为返回值都可以的。

我们可以看下官网，其中有一个简单的组件例子：

```javascript
<div>
	Hello {this.props.name}
</div>
```

这段代码会被转译成：

```javascript
React.createElement(
    "div",
    null,
    "Hello ",
    this.props.name
);
```

###### 属性

属性值可以为字符串：

```javascript
const element = <div name="nick"></div>
```

如果属性值为`JavaScript`表达式，需要加括号：

```javascript
const element = <img src={user.avatarUrl} />
```

大括号外面是不能加引号的，如果加了引号是会被当做字符串的。

##### className

在jsx中添加类名是需要使用className，而不是class。

```javascript
const element = <div class="box"></div>
```



###### jsx自动展开数组

jsx有着自动展开数组的特性

```javascript
const arr = [<p>哈</p>,<p>哈哈</p>,<p>哈哈哈</p>]
const elememt = {
	<div>{arr}</div>
}
//就相当于
<div>
	<p>哈</p>
	<p>哈哈</p>
	<p>哈哈哈</p>
</div>
```



###### 三元运算

```
{boolean ? <div>你好</div> : <div>你好啊</div>}
{boolean && <div>你好</div>}
```

###### 循环

在jsx中可以使用一些常见的JavaScript循环语法：

```javascript
const persons = [{name:'张三'},{name:'李四'}]

<ul>
	{person.map(person => <li>{person.name}</li>)}
</ul>
```



###### 事件

为jsx添加事件，需要指定事件名称和事件处理程序

```javascript
<div onclick={this.eventHandler}></div>
```

当给事件处理程序传递参数时，可以写成箭头函数的形式：

```javascript
<div onclick={ e => this.eventHandler('arg'，e)}></div>
```

或者是bind返回一个新的函数：

```javascript
<div onclick={this.eventHandler.bind(this,'arg')}></div>
```



###### 样式

为jsx添加样式，有以下几种：

- 行内样式

  ```javascript
  render(){
  	const style = {color:'red'}
  	return <div style={style}></div>
  }
  ```

  

- 外链样式

  ```javascript
  import styles from './css.css'
  
  render(){
  	return <div class.name={styles.div}></div>
  }
  ```

  

- 全局样式

  ```javascript
  import './css.css'
  ```

  

###### ref属性

当我们想要拿到组件对应的实例或者是对应的dom实例时，就需要用到这个属性了。

- createRef

  ```javascript
  class Input extends Component{
  	constructor(){
  		super()
  		this.inputRef = React.createRef()
  	}
  	render(){
  		return(
  			<div>
  				<input type='text'  ref={this.inputRef}/>
  				<button onclick={() => console.log(this.inputRef.current)}></button>
  			</div>	
  		)
  	}
  }
  ```

  

- 函数参数

  ```javascript
  class Input extends Component{
  	render(){
  		return(
  			<div>
  				<input type='text'  ref={ input => (this.input = input)}/>
  				<button onclick={() => console.log(this.input)}></button>
  			</div>	
  		)
  	}
  }
  ```

  这种将ref指定为一个函数，函数的参数就是我们的input的dom元素实例，然后将这个dom实例赋值给类的属性，随后就可以通过类的属性来访问到这个dom元素。

- ref字符串

  ```javascript
  <input type='text'  ref='username'/>
  // 这种可以通过 this.refs.username获取对应的实例，只不过在严格模式下会报错
  ```



##### 组件

react是基于组件的方式来对用户界面开发的，组件可以理解为对页面中的某一块区域的封装。

###### 创建组件

react中的组件分为类组件和函数组件

- 类组件

  ```javascript
  import React, {Component} from 'react'
  class App extends Component {
  	render() {
  		return <div>类组件</div>
  	}
  }
  ```

  

- 函数组件

  ```javascript
  const Person = () => {
  	return <div>函数组件</div>
  }
  ```

其中组件首字母必须大写，用以区分普通标签

jxs语法外层必须要有一个根元素

###### 组件的props

常见的父组件向子组件传递参数，就是通过props传递的

```javascript
<person name="nick"></person>
```

```javascript
//类组件
class Person extends Component{
	render(){
		return (
			<div>
				<h1>姓名：{this.props.name}</h1>
			</div>
		)
	}
}
```

```javascript
//函数组件
const Person = props => {
	return (
		<div>
			<h1>姓名：{this.props.name}</h1>
		</div>
	)
}
```

还可以给组件设置默认的props

```javascript
//类组件
class Person extends Component{
	static defaultProps = {...}
}
```

```javascript
//函数组件
const Person = props => {
}
Person.defaultProps = {...}
```

还可以通过props.children拿到组件调用时填充的内容。

```javascript
<person>组件中的内容</person>
```

```javascript
const Person = props => {
	return (
		<div>{props.children}</div>
	)
}
```



###### 类组件状态state

类组件除了能够从外部通过props接收状态数据以外还可以拥有自己的状态state，此状态在组件内部可以被更新，状态更新同样也会导致dom更新。组件内部的状态数据被存储在组件类的state属性中，state属性值为对象类型，属性名称固定不可更改。

```javascript
class Person extends Component{
	constructor(){
		super()
		this.state = {
			person:{name:'nick'}
		}
	}	
	render(){
		return (
			<div>
				<h1>姓名：{this.state.person.name}</h1>
			</div>
		)
	}
}
```

state状态对象中的数据不可直接更改，如果直接更改dom数据不会被更新，要更改state的数据需要使用setState方法。

```javascript
class App extends Component{
	constructor(){
		super()
		this.state = {
			name:'nick'
		}
        this.nameChanged = this.nameChanged.bind(this)
	}	
    nameChanged(e){
        this.setState({name:e.target.value})
    }
	render(){
		return (
			<div>
				<h1>姓名：{this.state.name}</h1>
				<Person name={this.state.name} changed={this.nameChanged}></Person>
			</div>
		)
	}
}
```

```javascript
const Person = props => {
	return <input type="text" value={props.name} onchange={props.changed}>
}
```



###### 类组件生命周期

react的生命周期主要分为三个阶段，挂载、更新和卸载。

- 挂载

  - constructor

    在组件挂载之前被调用，为React.Component子类实现构造函数时，首行调用super()。

  - getDerivedStateFromProps

    返回一个对象来更新state，如果返回null，则不更新任何内容。

  - render

    是class组件中唯一必须实现的方法，用于渲染dom，该方法中必须返回reactDom，常见的就是返回一个jsx对象。

    不能再该方法中使用setState方法，回导致死循环。

  - componentDidMount

    componentDidMount() 在组件挂载后 (插入DOM树后) 立即调用，componentDidMount() 是发送网络请求、启用事件监听方法的好时机，并且可以在 此钩子函数里直接调用 setState()

- 更新

  - shouldComponentUpdate

    在组件更新之前调用，可以控制组件是否进行更新， 返回true时组件更新， 返回false则不更新。

    不能再该方法中使用setState方法，回导致死循环。

  - getSnapshotBeforeUpdate 

    在最近一次的渲染输出被提交之前调用。也就是说，在 render 之后，即将对组件进行挂载时调用。 

  - componentDidUpdate

    会在更新后会被立即调用。首次渲染不会执行 

- 卸载

  - componentWillUnmount

    在组件即将被卸载或销毁时进行调用

###### Context

在涉及组件嵌套层级过深时，可以通过Context来实现跨层级传参

```javascript
//useContext.js
import React from 'react'

const userContext = React.createContext('default value')
const userProvider = userContext.Provider
const userConsumer = userContext.Consumer

export {userProvider,userConsumer}
```

```javascript
//App.js
import {userProvider} from './useContext'
class App extends Component{
    render(){
        return (
        	<userProvider value="hello react context"></userProvider>
        )
    }
}
```

```javascript
//c.js
import {userConsumer} from './useContext'

export calss c extends Component{
    render(){
        return (
        	<div>
            	<userConsumer>
            		{username => (
                    	return <div>{username}</div>
                     )}
            	</userConsumer>
            </div>
        )
    }
}


```



##### 路由

url地址与组件之间的对应关系，访问不同的url地址显示不同的组件。

###### 基本使用

```javascript
// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
function Index() {
	return <div>首页</div>;
}
function News() {
	return <div>新闻</div>;
}
function App() {
  return (
    <Router>
      <div>
        <Link to="/index">首页</Link>
        <Link to="/news">新闻</Link>
      </div>
      <div>
        <Route path="/index" component={Index}/>
        <Route path="/news" component={News}/>
      </div>
    </Router>
  );
}
```



###### 路由嵌套

```javascript
function News(props) {
  return (
    <div>
      <div>
        <Link to={`${props.match.url}/company`}>公司新闻</Link>
        <Link to={`${props.match.url}/industry`}>行业新闻</Link>
      </div>
      <div>
        <Route path={`${props.match.path}/company`} component={CompanyNews} />
        <Route path={`${props.match.path}/industry`} component={IndustryNews}/>  
      </div>	
    </div>
  );
}

function CompanyNews() {
	return <div>公司新闻</div>
}
function IndustryNews() {
	return <div>行业新闻</div>
}
```



###### 路由传参

```javascript
import url from 'url';
class News extends Component {
  constructor(props) {
    super(props);
    this.state = {
      list: [{
        id: 1,
        title: '新闻1'
      }, {
        id: 2,
        title: '新闻2'
      }]
    }
  }
    
  render() {
    return (
      <div>
        <div>新闻列表组件</div>
        <ul>
          this.state.list.map((item, index) => {
            return (
              <li key={index}>
                <Link to={`/detail?id=${item.id}`}>{item.title}</Link>
              </li>
            );
          })
        </ul>
      </div>
    );
  }
}
class Detail extends Component {
  constructor(props) {
    super(props);
  }
	const { query } = url.parse(this.props.location.search, true);
	console.log(query); // {id: 1}
  render() {
    return <div>新闻详情</div>
  }
}
```



###### 路由重定向

```javascript
import { Redirect } from 'react-router-dom';

class Login extends Component {
  render() {
    if (this.state.isLogin) {
      return <Redirect to="/"/>
    }
  }
}
```

