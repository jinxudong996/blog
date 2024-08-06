let str = 'aHR0cHM6Ly9kbGVyLnByby9hdXRoL3JlZ2lzdGVyP2FmZmlkPTg0MzEx'

function ba(str){
  let de = atob(str)
  let str1 = decodeURI(de)
  console.log(str1)
}

ba(str)