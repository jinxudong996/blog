学习脚手架需要用到两个插件commander和inpuier，文档地址为[commander](https://github.com/tj/commander.js/blob/master/Readme_zh-CN.md#commanderjs)和[inpuier](https://github.com/SBoudrias/Inquirer.js)

#### commander

>  完整的 [node.js](http://nodejs.org/) 命令行解决方案。 

首先安装`npm install commander`，新建`bin/index.js`，在第一行添加`#!/usr/bin/env node`，在`package.json`中添加

```
"bin": {
    "clipre": "bin/index.js"
  },
```

随后在根目录运行`npm link`，即可以通过在命令行运行`clipre`等各种命令。

##### 选项

首先要接受命令行传入的各种命令，可以使用`.option()`

> Commander 使用`.option()`方法来定义选项，同时可以附加选项的简介。每个选项可以定义一个短选项名称（-后面接单个字符）和一个长选项名称（--后面接一个或多个单词），使用逗号、空格或`|`分隔。
>
> 解析后的选项可以通过`Command`对象上的`.opts()`方法获取，同时会被传递给命令处理函数。可以使用`.getOptionValue()`和`.setOptionValue()`操作单个选项的值。

`bin/index.js`:

```javascript
#!/usr/bin/env node
const { program } = require('commander');
program.version('0.0.1');

program
  .option('-d, --debug', 'output extra debugging')
  .option('-s, --small', 'small pizza size')
  .option('-p, --pizza-type <type>', 'flavour of pizza');

program.parse(process.argv);

const options = program.opts();
if (options.debug) console.log(options);
console.log('pizza details:');
if (options.small) console.log('- small pizza size');
if (options.pizzaType) console.log(`- ${options.pizzaType}`);
```

在命令行输入`clipre -d -s -p vegetarian`，打印结果为

```
{ debug: true, small: true, pizzaType: 'vegetarian' }
pizza details:
- small pizza size
- vegetarian
```

同时还可以设置默认值：

```
.option('-a, --cheese <type>', 'add the specified type of cheese', 'blue');
```

通过`.requiredOption()`方法可以设置选项为必填。必填选项要么设有默认值，要么必须在命令行中输入，对应的属性字段在解析时必定会有赋值。该方法其余参数与`.option()`一致。 

```
.requiredOption('-c, --cheese <type>', 'pizza must have cheese');
```



选项的参数可以通过自定义函数来处理，该函数接收两个参数，即用户新输入的参数值和当前已有的参数值（即上一次调用自定义处理函数后的返回值），返回新的选项参数值。

自定义函数适用场景包括参数类型转换，参数暂存，或者其他自定义处理的场景

可以在自定义函数的后面设置选项参数的默认值或初始值 

```javascript
function myParseInt(value, dummyPrevious) {
  // parseInt 参数为字符串和进制数
  const parsedValue = parseInt(value, 10);
  if (isNaN(parsedValue)) {
    throw new commander.InvalidArgumentError('Not a number.');
  }
  return parsedValue;
}

function increaseVerbosity(dummyValue, previous) {
  return previous + 1;
}

function collect(value, previous) {
  return previous.concat([value]);
}

function commaSeparatedList(value, dummyPrevious) {
  return value.split(',');
}

program
  .option('-f, --float <number>', 'float argument', parseFloat)
  .option('-i, --integer <number>', 'integer argument', myParseInt)
  .option('-v, --verbose', 'verbosity that can be increased', increaseVerbosity, 0)
  .option('-c, --collect <value>', 'repeatable value', collect, [])
  .option('-l, --list <items>', 'comma separated list', commaSeparatedList)
;

program.parse();

const options = program.opts();
if (options.float !== undefined) console.log(`float: ${options.float}`);
if (options.integer !== undefined) console.log(`integer: ${options.integer}`);
if (options.verbose > 0) console.log(`verbosity: ${options.verbose}`);
if (options.collect.length > 0) console.log(options.collect);
if (options.list !== undefined) console.log(options.list);
```

##### 命令

通过`.command()`或`.addCommand()`可以配置命令，有两种实现方式：为命令绑定处理函数，或者将命令单独写成一个可执行文件。

`.command()`的第一个参数为命令名称。命令参数可以跟在名称后面，也可以用`.argument()`单独指定。参数可为必选的（尖括号表示）、可选的（方括号表示）或变长参数（点号表示，如果使用，只能是最后一个参数）。 

```javascript
#!/usr/bin/env node
const { program } = require('commander');

program
  .version('0.1.0')
  .argument('<username>', 'user to login')
  .argument('[password]', 'password for user, if required', 'no password given')
  .action((username, password) => {
    console.log('username:', username);
    console.log('password:', password);
  });
  
  program.parse();

//命令行输入
clipre nick 123
//打印结果
username: nick
password: 123
```

 在参数名后加上`...`来声明可变参数，且只有最后一个参数支持这种用法。可变参数会以数组的形式传递给处理函数 

```javascript
program
  .version('0.1.0')
  .command('rmdir')
  .argument('<dirs...>')
  .action(function (dirs) {
    dirs.forEach((dir) => {
      console.log('rmdir %s', dir);
    });
  });

//命令行输入
clipre rmdir nickasd 12
//打印结果
rmdir nickasd
rmdir 12
```

##### 帮助信息

帮助信息是 Commander 基于你的程序自动生成的，默认的帮助选项是`-h,--help`。 

```
Usage: index [options]

Options:
	-h, --help  display help for command
```

 如果你的命令中包含了子命令，会默认添加`help`命令，同时也可以使用`addHelpText（）`添加额外信息。

```javascript
program
  .option('-f, --foo', 'enable some foo');

program.addHelpText('after', `
Example call:
  $ custom-help --help`);

//命令行输入
clipre -h
//打印结果
Usage: index [options]

Options:
  -f, --foo   enable some foo
  -h, --help  display help for command

Example call:
  $ custom-help --help
```



#### inpuier

>  一组常见的交互式命令行用户界面 
>

安装`npm install inquirer`，常用的方法有：

- prompt 启动命令界面，参数有

  - questions，是一个数组，包含问题对象，也可以传递一个 Rx.Observable 实例 
  -  answers， 包含已回答问题的值。询问者将避免询问这里已经提供的答案。默认值 {} 

  返回一个promise。

- registerPrompt，注册插件，参数有
  - name，插件名字
  - prompt -提示对象
- createPromptModule， 创建一个自包含的查询器模块。如果您不想在覆盖或添加新提示类型时影响其他也依赖查询器的库 

这是一个挑选披萨的例子

```javascript
const inquirer = require('inquirer');

inquirer
  .prompt([
    {
      type: 'checkbox',
      message: 'Select toppings',
      name: 'toppings',
      choices: [
        new inquirer.Separator(' = The Meats = '),
        {
          name: 'Pepperoni',
        },
        {
          name: 'Ham',
        },
        {
          name: 'Ground Meat',
        },
        {
          name: 'Bacon',
        },
        new inquirer.Separator(' = The Cheeses = '),
        {
          name: 'Mozzarella',
          checked: true,
        },
        {
          name: 'Cheddar',
        },
        {
          name: 'Parmesan',
        },
        new inquirer.Separator(' = The usual ='),
        {
          name: 'Mushroom',
        },
        {
          name: 'Tomato',
        },
        new inquirer.Separator(' = The extras = '),
        {
          name: 'Pineapple',
        },
        {
          name: 'Olives',
          disabled: 'out of stock',
        },
        {
          name: 'Extra cheese',
        },
      ],
      validate(answer) {
        if (answer.length < 1) {
          return 'You must choose at least one topping.';
        }

        return true;
      },
    },
  ])
  .then((answers) => {
    console.log(JSON.stringify(answers, null, '  '));
  });
```

在命令行运行clipre，即可以问题选项，最后将`answers`转化为字符串打印出来。

启动命令界面的`prompt()`方法接受一个questions数组，包含问题对象，问题对象常用的属性有：

- type，常用的类型有 `input`, `number`, `confirm`, `list`, `rawlist`, `expand`, `checkbox`, `password`, `editor` 
- name，名称
-  message， 要打印的问题。如果定义为函数，第一个参数将是当前查询器会话的答案。默认为 name 的值 
- choices ， 选择数组或返回选择数组的函数。如果定义为函数，第一个参数将是当前查询器会话的答案。数组值可以是简单的数字、字符串或包含名称（以显示在列表中）、值（以保存在答案散列中）和简短（以在选择后显示）属性的对象。选择数组还可以包含一个分隔符 
-  validate，校验函数。 









