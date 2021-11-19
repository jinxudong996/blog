#!/usr/bin/env node

const pkg = require('./package.json')
checkVersion() //检查版本


function checkVersion() {
  console.log(pkg.version)
}