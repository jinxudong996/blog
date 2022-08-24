"use strict";
exports.__esModule = true;
var Dong = /** @class */ (function () {
    function Dong() {
        this.name = "dong";
    }
    Dong.prototype.hello = function () {
        return 'hello, I\'m ' + this.name;
    };
    return Dong;
}());
var dong = new Dong();
console.log(dong.hello.call({ name1: 123 }));
