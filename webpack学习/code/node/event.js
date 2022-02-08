// const EventEmitter = require('events')

// const ev = new EventEmitter()

// ev.on('事件1',() => {
//     console.log('事件1执行')
// })

// ev.emit('事件1')

setTimeout(() =>{
    console.log('s1')
    Promise.resolve().then(() => {
        console.log('p1')
    })
    Promise.resolve().then(() => {
        console.log('p2')
    })
})

setTimeout(() =>{
    console.log('s2')
    Promise.resolve().then(() => {
        console.log('p3')
    })
    Promise.resolve().then(() => {
        console.log('p4')
    })
})