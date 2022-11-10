


let data = [
  { "name": "Adil", "recentlyPlayedWith": ["Ben", "Andy", "Rio", "Nader", "Giuliano", "Walter", "Dali"] }, 
  { "name": "Andy", "recentlyPlayedWith": ["Adil", "Walter", "Chris", "Dan", "Ben"] }, 
  { "name": "Dan", "recentlyPlayedWith": ["Andy", "Rio", "Dennis", "John", "Bernard", "Ben"] }, 
  { "name": "Ben", "recentlyPlayedWith": ["Nader", "Dali", "Dan", "Carter", "Bruno", "Andy", "Adil"] }, 
  { "name": "Nader", "recentlyPlayedWith": ["Adil", "Ben", "Arthur"] }, 
]


function findFrend(arr){
  let frendArr = []
  let frendAllArr = []
  // 拿到所有的两两组合
  arr.map((item,index) => {
    item.recentlyPlayedWith.map(itemChild => {
        frendAllArr.push([item.name,itemChild])
    })
  })
  // 遍历两两组合
  console.log(frendAllArr.length)
  // return frendArr;
}

function select

findFrend(data)
// console.log()