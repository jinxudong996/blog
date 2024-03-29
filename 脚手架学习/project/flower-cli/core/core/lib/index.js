'use strict';

module.exports = core;

const userHome = require('user-home')
const path = require('path')
const fs = require('fs');
const semver = require('semver')
const commander = require('commander')
const color = require('colors/safe')

const pkg = require('../../../package.json')
const log = require('@flower-cli/log')
const init = require('@flower-cli/init')

let args, config

const program = new commander.Command()

function core() {
  // try {
    checkVersion()
    checkNodeVersion()
    // checkRoot()
    checkUserHome()
    // checkInputArgs()
    checkEnv()
    checkGlobalUpdate()

    registerCommand()
  // } catch (e) {
  //   log.error(e)
  // }

}

function checkVersion() {
  log.notice('flower-cli', pkg.version)
}

function checkNodeVersion() {
  const currentVersion = process.version;
  const lowestVersion = '13.0.0';
  if (!semver.gte(currentVersion, lowestVersion)) {
    throw new Error(color.red(`flower-cli需要安装 v${lowestVersion}以上版本`))
  }
}

function checkRoot() {
  const rootCheck = require('root-check')
  rootCheck()
  // console.log(process.geteuid())
}

function checkUserHome() {
  // console.log(userHome)
  if (fs.existsSync(userHome)) {
    console.log('主目录存在')
  } else {
    throw new Error(color.red('当前用户主目录不存在'))
  }
}

function checkInputArgs() {
  const minimist = require('minimist');
  args = minimist(process.argv.slice(2))
  checkArgs()
}

function checkArgs() {
  if (args.debug) {
    process.env.LOG_LEVEL = 'verbose'
  } else {
    process.env.LOG_LEVEL = 'info'
  }
  log.level = process.env.LOG_LEVEL
}

function checkEnv() {
  const dotenv = require('dotenv')
  const dotenvPath = path.resolve(userHome, '.env')
  config = dotenv.config({
    path: dotenvPath
  })
  log.verbose('环境变量', config, process.env.name)
}

async function checkGlobalUpdate() {
  const { getNpmSemverVersion } = require('@flower-cli/get-npm-info')
  const currentVersion = pkg.version
  const npmName = pkg.name
  const lastVersions = await getNpmSemverVersion(currentVersion, npmName)
  if (lastVersions && semver.gt(lastVersions, currentVersion)) {
    log.warn(color.yellow(`请手动更新${npmName}，当前版本：${currentVersion}，最新版本：${lastVersions}`))
  }
}

function registerCommand() {
  program
    .name('flower-cli')
    .usage('<command> [options]')
    .version(pkg.version)
    .option('-d, --debug', '是否开启调试模式', false)

  program
    .command('init [projectName]')
    .option('-f,--force','是否强制初始化项目')
    .action(init)

  program.on('option:debug', function () {
    if(program._optionValues.debug){
      process.env.LOG_LEVEL = 'verbose'
    }else{
      process.env.LOG_LEVEL = 'info'
    }
    log.level = process.env.LOG_LEVEL
  })
  program.on('command:*',function(obj){
    const avalibleCommands = program.commands.map(cmd => cmd.name())
    console.log(color.red('未知的命令：' + obj[0]));
    if(avalibleCommands.length > 0){
      console.log(color.red('可用命令' + avalibleCommands.join('.')))
    }
  })

  if(process.argv.length < 3){
    program.outputHelp()
    console.log()
  }
  program.parse(process.argv)
}