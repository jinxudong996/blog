let obj = {
    '.js'(){
        console.log('123')
    },
    '.json'(){}
}

console.log(obj['.js']())