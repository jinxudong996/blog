function defineReactive (obj, key, val) {
    Object.defineProperty(obj, key, {
        enumerable: true,       /* 属性可枚举 */
        configurable: true,     /* 属性可被修改或删除 */
        get: function reactiveGetter () {
            return val;        
        },
        set: function reactiveSetter (newVal) {
            if (newVal === val) return;
            console.log('更新了视图。。。' + newVal);
        }
    });
}

function observer (value) {
    if (!value || (typeof value !== 'object')) {
        return;
    }

    Object.keys(value).forEach((key) => {
        defineReactive(value, key, value[key]);
    });
}

class Vue {
    constructor(options) {
        this._data = options.data;
        observer(this._data);
    }
}

let o = new Vue({
    data: {
        test: "I am test."
    }
});
o._data.test = "hello,world.";