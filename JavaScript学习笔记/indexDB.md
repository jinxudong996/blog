#### IndexedBD

> Indexed Database API 简称 IndexedDB，是浏览器中存储结构化数据的一个方案。IndexedDB 用于代 替目前已废弃的 Web SQL Database API。IndexedDB 背后的思想是创造一套 API，方便 JavaScript 对象的 存储和获取，同时也支持查询和搜索 

##### 数据库

> IndexedDB 是类似于 MySQL 或 Web SQL Database 的数据库。与传统数据库最大的区别在于， IndexedDB 使用对象存储而不是表格保存数据。IndexedDB 数据库就是在一个公共命名空间下的一组对 象存储，类似于 NoSQL 风格的实现。 

```javascript
let db,
  request,
  version = 1;
request = indexedDB.open("admin", version);
request.onerror = (event) =>
 console.log(`Failed to open: ${event.target.errorCode}`);
request.onsuccess = (event) => {
 db = event.target.result;
 console.log(db)
}; 
console.log(request)
```

调用 indexedDB.open()方法，并给它传入一个要打开的数据 库名称。如果给定名称的数据库已存在，则会发送一个打开它的请求；如果不存在，则会发送创建并打开这个数据库的请求。这个方法会返回 IDBRequest 的实例，可以在这个实例上添加 onerror 和 onsuccess 事件处理程序。 

在两个事件处理程序中，event.target 都指向 request，因此使用哪个都可以。如果 onsuccess 事件处理程序被调用，说明可以通过 event.target.result 访问数据库（IDBDatabase）实例了， 这个实例会保存到 db 变量中。之后，所有与数据库相关的操作都要通过 db 对象本身来进行。如果打 开数据库期间发生错误，event.target.errorCode 中就会存储表示问题的错误码。 

##### 对象存储

```javascript
let db,
 	request,
  	version = 3;
let user = {
 	username: "007",
 	firstName: "James",
 	lastName: "Bond",
 	password: "foo"
};
request = indexedDB.open("admin", version);
request.onerror = (event) =>
 onsole.log(`Failed to open: ${event.target.errorCode}`);
request.onsuccess = (event) => {
	db = event.target.result;
	console.log(db)
}; 
request.onupgradeneeded = (event) => {
    const db = event.target.result;
    // 如果存在则删除当前 objectStore。测试的时候可以这样做
    // 但这样会在每次执行事件处理程序时删除已有数据
    if (db.objectStoreNames.contains("users")) {
 		db.deleteObjectStore("users");
	}
	db.createObjectStore("users", { keyPath: "username" });
	console.log(db)
}; 
```

数据库的版本决定了数据库模式，包括数据库中的对象存储和这些对象存储的结构。如果数据库还 不存在，open()操作会创建一个新数据库，然后触发 upgradeneeded 事件。可以为这个事件设置处 理程序，并在处理程序中创建数据库模式。如果数据库存在，而你指定了一个升级版的版本号（版本号必须为正整数），则会立 即触发 upgradeneeded 事件，因而可以在事件处理程序中更新数据库模式。

keyPath 属性表示应该用作键的存储对象的属性名 。



##### 事务

创建了对象存储之后，剩下的所有操作都是通过事务完成的。事务要通过调用数据库对象的 transaction()方法创建。任何时候，只要想要读取或修改数据，都要通过事务把所有修改操作组织起来。 

```
let transaction = db.transaction(); 
```

 如果不指定参数，则对数据库中所有的对象存储有只读权限。更具体的方式是指定一个或多个要访 问的对象存储的名称： 

```
let transaction = db.transaction("users");

let transaction = db.transaction(["users", "anotherStore"]);
```

还可以传入第二个参数来设置访问权限，第二个参数有 `readonly`、`readwrite`或`versionchange` 

```
let transaction = db.transaction("users", "readwrite");
```

 这样事务就可以对 users 对象存储读写了。 

有了事务的引用，就可以使用 objectStore()方法并传入对象存储的名称以访问特定的对象存储。 然后，可以使用 add()和 put()方法添加和更新对象，使用 get()取得对象，使用 delete()删除对象， 使用 clear()删除所有对象。

 



##### 插入对象

拿到了对象存储的引用后，就可以使用 add()或 put()写入数据了。这两个方法都接收一个参数， 即要存储的对象，并把对象保存到对象存储。这两个方法只在对象存储中已存在同名的键时有区别。这 种情况下，add()会导致错误，而 put()会简单地重写该对象。更简单地说，可以把 add()想象成插入 新值，而把 put()想象为更新值。 





##### 通过游标查询





##### 键范围





##### 设置游标方向







##### 索引





##### 并发问题





##### 限制