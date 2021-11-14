interface SearchFunc {
  (source: string, subString: string): boolean
}

let mySearch: SearchFunc
mySearch = function(source: string, subString: string): boolean {
  let result = source.search(subString);
  return result > -1
}