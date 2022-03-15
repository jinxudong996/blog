'use strict';

const axios = require('axios')
const urlJoin = require('url-join')
const semver = require('semver')

function getNpmInfo(npmName, registry) {
  if (!npmName) {
    return null
  }
  const registryUrl = registry || getDefaultRegistry()
  const npmInfoUrl = urlJoin(registryUrl, npmName,'core')
  
  return axios.get(npmInfoUrl).then(res => {
    if (res.status == 200) {
      return res.data
    } else {
      return null
    }
  })
}

function getDefaultRegistry(isOriginal = false) {
  return isOriginal ? 'https://registry.npmjs.org' : 'https://registry.npm.taobao.org'
}

async function getNpmVersion(npmName, registry) {
  const data = await getNpmInfo(npmName,registry)
  if(data){
    return Object.keys(data.versions)
  }else{
    return []
  }
}

//获取满足条件的版本号
function getSemverVersions(baseVersion,version){
  return version
    .filter(v => semver.satisfies(v,`^${baseVersion}`))
    .sort((a,b) => semver.gt(b,a))
}

async function getNpmSemverVersion(baseVersion,npmName,registry){
  const versions = await getNpmVersion(npmName,registry)
  const newVersions = getSemverVersions(baseVersion,versions)
  if(newVersions && newVersions.length > 0){
    return newVersions[newVersions.length -1]
  }
}


module.exports = { 
  getNpmInfo,
  getNpmVersion,
  getNpmSemverVersion,

};