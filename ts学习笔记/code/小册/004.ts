function identity<Type>(arg: Type[]): Type[] {
  console.log(arg.length)
  return arg;
}
console.log(identity(['asd']))

function identity1<Type>(arg: Type): Type {
  return arg;
}
 
let myIdentity: <Type>(arg: Type) => Type = identity1;