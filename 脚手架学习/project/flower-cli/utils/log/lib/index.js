'use strict';

const log = require('npmlog')

log.level = process.env.LOG_LEVEL ? process.env.LOG_LEVEL : 'info'; //判断debugger模式

log.heading = 'flower'; //修改前缀
log.addLevel('success',2000,{fg:'green',blod:true}) //添加自定义指令

module.exports = log;

