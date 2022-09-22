import { init } from 'snabbdom/build/package/init'
import { h } from 'snabbdom/build/package/h'

const patch = init([])
let vnode = h('div#app', 'Hello world1')
const app = document.getElementById('app')
patch(app, vnode)