const userList = [];
function emit(newValue) {
  console.log(newValue);
}
const proxy = new Proxy(userList, {
  set(target, property, value, receiver) {
    const result = Reflect.set(...arguments);
    if (result) {
      emit(Reflect.get(target, property, receiver));
    }
    return result;
  }
});
proxy.push('John');

proxy.push('Jacob');
console.log(userList)
// John
// 1
// Jacob
// 2