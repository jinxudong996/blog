let date = {
  name:'nick',
  age:'18'
}
// for(let i in date){
//   console.log(i)
//   console.log(date[i])
// }
function reportWithIMG(url,data){
  // var img = new Image();
  // img.width = 1;
  // img.height = 1;
  console.log(data)
  let str = ''
  for(let item in data){
    console.log(item)
    console.log(data[item])
    str += item + '=' + data[item] + '&'
  }
  console.log(1111,str)
  // img.src = '/sa.gif?project=default&data=xxx'
}

reportWithIMG(1,date)