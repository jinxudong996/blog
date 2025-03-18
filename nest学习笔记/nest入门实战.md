

Nest 是一个用于构建高效，可扩展的 [Node.js](http://nodejs.cn/) 服务器端应用程序的框架。它使用渐进式 JavaScript，内置并完全支持 [TypeScript](https://www.tslang.cn/)（但仍然允许开发人员使用纯 JavaScript 编写代码）并结合了 OOP（面向对象编程），FP（函数式编程）和 FRP（函数式响应编程）的元素。 

##### 安装

首先安装官方的脚手架

```
npm i -g @nestjs/cli
nest new project-name
```

就可以看到src下面有一些核心文件

| app.controller.ts      | 带有单个路由的基本控制器示例。                               |
| ---------------------- | ------------------------------------------------------------ |
| app.controller.spec.ts | 对于基本控制器的单元测试样例                                 |
| app.module.ts          | 应用程序的根模块。                                           |
| app.service.ts         | 带有单个方法的基本服务                                       |
| main.ts                | 应用程序入口文件。它使用 `NestFactory` 用来创建 Nest 应用实例。 |

 `NestJS` 有一个核心概念就是模块化：采用模块化的架构，使得代码组织清晰，易于维护和扩展。   

看一下脚手架生成的`app.module.ts`

```js
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

这里的`AppModule`就是根模块，`AppController`是一个控制器，`AppService`是一个服务，提供业务逻辑。如果我们需要使用其他模块，可以在`imports: [],`进行导入。

实际上`nest`中的模块，可以理解为前端中的组件，项目都是由模块或则组件搭建起来的。

接下来通过命令来创建一个`user`模块

```
nest generate resource user
```

这是生成一个完整的模块的代码，实际上也可以逐个生成

```
# 创建 User 模块
nest generate module user

# 创建 User 服务
nest generate service user

# 创建 User 控制器
nest generate controller user
```

我们选择使用创建完整的模块，然后选择REST 风格 api和 生成 CRUD 代码

然后就会自动在根模块`app.module.ts` 中自动引入刚刚创建的模块

```
import { UserModule } from './user/user.module';

imports: [UserModule, LogModule],
```

同时还会常见`src/user/dto`文件夹和`src/user/entities`文件，

1.  `dto` 目录用于存放数据传输对象（Data Transfer Objects）。DTO 用于定义在客户端和服务器之间传输的数据结构，确保数据的完整性和安全性。 

   比如

   ```js
   export class CreateUserDto {
     name: string;
     email: string;
     password: string;
   }
   
   export class UpdateUserDto {
     name?: string;
     email?: string;
     password?: string;
   }
   ```

2.  `entities/` 目录用于存放实体类（Entities）。实体类通常与数据库表对应，用于定义数据库表的结构和字段。 

   比如

   ```js
   import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';
   
   @Entity()
   export class User {
     @PrimaryGeneratedColumn()
     id: number;
   
     @Column()
     name: string;
   
     @Column()
     email: string;
   
     @Column()
     password: string;
   }
   ```

还会创建一些文件：

1. user.controller.ts    控制器用于处理 HTTP 请求并返回响应。它定义了路由和处理逻辑 
2. user.module.ts    模块用于组织和封装相关的功能。它定义了模块的导入、导出、控制器和服务 
3. user.service.ts   服务用于处理业务逻辑。它通常与数据库交互，执行数据操作。 
4. user.service.spec.ts   服务的测试文件，用于编写单元测试 

再次总结下Nest模块化的概念：

- **模块（Module）**：模块是组织代码的基本单元，通常每个模块负责一个特定的功能或业务逻辑。模块通过 `@Module` 装饰器定义，并且可以包含控制器、服务、提供者等。
- **根模块（Root Module）**：每个 NestJS 应用程序都有一个根模块，通常是 `AppModule`。这个模块是应用程序的入口点，负责引导整个应用的启动过程。
- **导入模块（Import Modules）**：模块可以通过 `imports` 数组导入其他模块，从而共享这些模块中的提供者和服务。这种方式促进了代码的复用和解耦。
- **导出提供者（Export Providers）**：如果一个模块中的提供者需要被其他模块使用，可以通过 `exports` 数组将其导出。这样，其他模块在导入该模块时就可以访问这些提供者。
- **全局模块（Global Modules）**：某些模块可能需要在整个应用程序中可用。可以通过设置 `@Global()` 装饰器将模块标记为全局模块，这样就不需要在每个模块中重复导入它。

##### 核心思想

在Nest中， AOP（面向切面编程）和 IoC（控制反转）是两个重要的概念，可以让我们更好地组织和管理代码，提高代码的可维护性和可扩展性。 

###### AOP

 **控制反转** 是一种设计原则，它将对象的创建和管理从应用程序代码中分离出来，交给外部容器来处理。在 NestJS 中，IoC 主要通过依赖注入（Dependency Injection, DI）来实现。 

以上面常见的user模块来说，

```js
// user.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  findAll() {
    return `This action returns all user`;
  }
}
```

```js
// user.controller.ts
import { Controller, Get } from '@nestjs/common';
import { UserService } from './user.service';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  findAll() {
    return this.userService.findAll();
  }
}
```

这里`UserService`就是一个提供者， 通过构造函数注入到 `UserController` 中 ，当我们访问`http://localhost:3000/user`时就会调用在`UserService`中定义的findAll方法。

###### IOC

 **面向切面编程** 是一种编程范式，它允许你将横切关注点（如日志记录、事务管理、权限校验等）与业务逻辑分离。AOP 通过定义切面（Aspects）来实现这些横切关注点，并将它们应用到应用程序的不同部分。 

为了扩展功能而不影响原有的业务逻辑而实现的，神光的[册子](https://juejin.cn/book/7226988578700525605/section/7227320664649105463#heading-0)这个章节写的很清楚。





##### 装饰器







##### 中间件





##### 管道





##### 文件配置

当涉及数据库地址、密码等重要的字段时，不能放在代码里，需要存放在本地，通过设置不同的环境变量来读取对应的内容，就和我们前端配置webpack类似，设置不同的请求地址。官方提供了这样一个库` @nestjs/config `

```
yarn add  @nestjs/config
yarn add  cross-env
```

新建指定文件

```
.env.production
DATABASE_HOST=proddb.example.com
DATABASE_PORT=5500

.env.test
DATABASE_HOST=localhost
DATABASE_PORT=5400
```

然后更改下运行命令

```
"start:pro": "cross-env NODE_ENV=production nest start",
"start:dev": "cross-env NODE_ENV=test nest start --watch",
```

这时就可以在代码里正常读取设置的变量了

比如在`user.controller.ts`

```js
import { ConfigService } from '@nestjs/config';

。。。
@Get()
  findAll() {
    const environment = this.configService.get<string>('NODE_ENV');
    const host = this.configService.get<string>('DATABASE_HOST');
    const prot = this.configService.get<string>('DATABASE_PORT');
    console.log(`Current environment: ${environment}`);
    console.log(`Current DATABASE_HOST: ${host}`);
    console.log(`Current DATABASE_PORT: ${prot}`);
    return this.userService.findAll();
  }
```

用浏览器访问`http://localhost:3000/user`就可以看到控制台指定输出了。



##### 连接数据库

这里我们使用typeorm来连接mysql数据库，已经在我的云服务器上创建了个docker镜像，安装了mysql，创建了一个test数据库。

###### 安装依赖

```
yarn add @nestjs/typeorm typeorm mysql2
```

###### 配置TypeORM

```JS
app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserModule } from './user/user.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'mysql',
      host: 'yourhost',
      port: 3306,
      username: 'root',
      password: 'my-secret',
      database: 'test',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: true, // 注意：生产环境中不建议使用
    }),
    UserModule,
  ],
})
export class AppModule {}
```

###### 创建实体

```js
//  src/user/user.entity.ts
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  email: string;
}
```

这里定义了数据表的结构，id作为主键，还有name字段和email字段

###### 创建服务

```js
//  src/user/user.service.ts
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }

  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  async findOne(id: number): Promise<User> {
    return this.usersRepository.findOneBy({ id });
  }

  async update(id: number, updateUserDto: UpdateUserDto): Promise<User> {
    await this.usersRepository.update(id, updateUserDto);
    return this.usersRepository.findOneBy({ id });
  }

  async remove(id: number): Promise<void> {
    await this.usersRepository.delete(id);
  }
}
```

service用来处理业务逻辑

###### 创建DTO

 DTO用于定义请求和响应的数据结构。 

```js
//  src/user/dto/create-user.dto.ts
export class CreateUserDto {
  name: string;
  email: string;
}

//  src/user/dto/update-user.dto.ts
export class UpdateUserDto {
  name?: string;
  email?: string;
}
```

###### 更新控制器

 控制器用于处理HTTP请求。 

```js
//src/user/user.controller.ts
import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { UserService } from './user.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  @Get()
  findAll() {
    return this.userService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.userService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.userService.update(+id, updateUserDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.userService.remove(+id);
  }
}
```

###### 更新模块

 确保`UserModule`正确导入了`TypeOrmModule`和相关的实体。 

```js
// src/user/user.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity';
import { UserService } from './user.service';
import { UserController } from './user.controller';

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  providers: [UserService],
  controllers: [UserController],
})
export class UserModule {}
```

###### 测试

一共创建了五个接口

| 请求方法 | 地址                             | 描述         |
| :------- | :------------------------------- | :----------- |
| POST     | `http://localhost:3000/user`     | 创建新用户   |
| GET      | `http://localhost:3000/user`     | 获取所有用户 |
| GET      | `http://localhost:3000/user/:id` | 获取单个用户 |
| PATCH    | `http://localhost:3000/user/:id` | 更新用户     |
| DELETE   | `http://localhost:3000/user/:id` | 删除用户     |

用浏览器和apifix对接口进行测试，都没问题。



###### 连表查询

 连表查询（Join Query）是指在数据库中从多个表中检索数据，并根据某些条件将这些表连接在一起。连表查询在关系型数据库中非常常见，用于获取相关联的数据。 

当前我们已经有了user，再新建一个message表，通过user表中的id关联起来

```js
//message.entity.ts
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { User } from './user.entity';

@Entity()
export class Message {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  content: string;

  @ManyToOne(() => User, (user) => user.messages)
  @JoinColumn({ name: 'user_id' })
  user: User;
}

//user.entity.ts
import { Entity, Column, PrimaryGeneratedColumn, OneToMany } from 'typeorm';
import { Message } from './message.entity';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column()
  email: string;

  @OneToMany(() => Message, (message) => message.user)
  messages: Message[];
}

```

 `@Entity()` 是 TypeORM 提供的一个装饰器（Decorator），用于将一个类标记为数据库中的一个实体（Entity）。在 TypeORM 中，实体通常对应数据库中的一张表。 

·`@OneToMany(() => Message, (message) => message.user)`

`@OneToMany()` 是 TypeORM 提供的一个关系装饰器，用于定义实体之间的“一对多”关系。在这个例子中，它定义了 `User` 实体和 `Message` 实体之间的关系：一个用户（`User`）可以有多个消息（`Message`）。

这样就创建好了message表，然后再插入一些测试数据，这时两张表是这样

```
mysql> SELECT * FROM user;
+----+---------+---------------------+
| id | name    | email               |
+----+---------+---------------------+
|  1 | Alice   | alice@example.com   |
|  2 | Bob     | bob@example.com     |
|  3 | Charlie | charlie@example.com |
|  4 | Alice   | alice@example.com   |
|  5 | daya    | 123asd@qq.com       |
+----+---------+---------------------+

mysql> SELECT * FROM  message;
+----+-------------------+---------+
| id | content           | user_id |
+----+-------------------+---------+
|  1 | Hello, World!     |       1 |
|  2 | How are you?      |       1 |
|  3 | Nice to meet you. |       2 |
+----+-------------------+---------+
```

如果用用mysql语句来做连表查询是这样的

```js
SELECT user.id, user.name, message.content FROM user INNER JOIN message ON user.id = message.user_id;

+----+-------+-------------------+
| id | name  | content           |
+----+-------+-------------------+
|  1 | Alice | Hello, World!     |
|  1 | Alice | How are you?      |
|  2 | Bob   | Nice to meet you. |
+----+-------+-------------------+
```

 然后在TypeORM 中，可以使用 `Repository` 和 `QueryBuilder` 来进行连表查询。 

```js
export class UserService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
    @InjectRepository(Message)
    private messagesRepository: Repository<Message>,
  ) {}
  async findAll(): Promise<User[]> {
    return this.usersRepository.find({
      relations: ['messages'],
    });
  }
  async findUserMessages(userId: number): Promise<User> {
    return this.usersRepository
      .createQueryBuilder('user')
      .where('user.id = :userId', { userId })
      .leftJoinAndSelect('user.messages', 'message')
      .getOne();
  }
}
```

在` UserService  `中定义查询方法，然后访问`http://localhost:3000/user`，就可以看到连表查询的内容了

```json
{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "messages": [
      {
        "id": 2,
        "content": "How are you?"
      },
      {
        "id": 1,
        "content": "Hello, World!"
      }
    ]
  },
  {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com",
    "messages": [
      {
        "id": 3,
        "content": "Nice to meet you."
      }
    ]
  },
。。。
```

然后在`user.controller.ts`中定义下接口

```js
@Get(':id/messages')
  findUserMessages(@Param('id') id: string) {
    return this.userService.findUserMessages(+id);
  }
```

用浏览器访问下`http://localhost:3000/user/1/messages`

```js
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "messages": [
    {
      "id": 1,
      "content": "Hello, World!"
    },
    {
      "id": 2,
      "content": "How are you?"
    }
  ]
}
```



##### 调试





##### 日志