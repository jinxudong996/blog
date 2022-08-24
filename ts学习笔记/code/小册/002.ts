
export {}
class Dong {
  name: string;

  constructor() {
      this.name = "dong";
  }

  hello() {
      return 'hello, I\'m ' + this.name;
  }
}

const dong = new Dong();
console.log(dong.hello.call({name1:123}));