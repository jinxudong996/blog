#### 安装使用

 最快捷的创建 Next.js 项目的方式是使用 `create-next-app`脚手架 ，运行

```
npx create-next-app
```

然后设置项目名称，是否使用typescript，开启eslint等，根据自己项目需要选择yes或者no即可。

随后运行`http://localhost:3000/`就可以看到项目已经跑起来了。

#### 路由

 Next.js 有两套路由解决方案，之前的方案称之为“Pages Router”，目前的方案称之为“App Router”，两套方案目前是兼容的，都可以在 Next.js 中使用。  v13.4 起，App Router 已成为默认的路由方案 。

##### Pages Router

 Next.js 的路由基于的是文件系统 ， 一个文件就可以是一个路由 。

在根目录或者src目录下新建一个pages目录，改目录下的所有的js文件都会被解析成路由。

新建`src/pages/about.js`

```js
import React from 'react'
export default () => <h1>Hello world,this is about page</h1>
```





##### App Router

 App Router使用文件夹来定义路由。每个文件夹都代表一个对应到 URL 片段的路由片段。 

定义文件`app/detail/page.tsx`，

```js
export default function Page() {
  return <h1>Hello world,this is detail page</h1>
}
```

这个路由就对应着`detail`，即访问`http://localhost:3000/detail`，而定义文件page.tsx，则是一种约定俗成。

App route还有定义了布局、模板、加载loading、错误处理和404页面，接下来逐个学习下。

###### 布局

布局是指多个页面共享的 UI。在导航的时候，布局会保留状态、保持可交互性并且不会重新渲染，比如用来实现后台管理系统的侧边导航栏。

定义文件`app/dashboard/alyout.tsx`

```ts
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <section>
      <nav>nav</nav>
      {children}
    </section>
  );
}
```

定义文件`app/dashboard/page.tsx`

```ts
export default function Page() {
  return <h1>Hello, Dashboard!</h1>
}
```

当访问`http://localhost:3000/dashboard`时，就可以看到nav和Hello, Dashboard!的内容。

 同一文件夹下如果有 layout.js 和 page.js，page 会作为 children 参数传入 layout。换句话说，layout 会包裹同层级的 page。



###### 模板

模板类似于布局，它也会传入每个子布局或者页面。但不会像布局那样维持状态。 

模板在路由切换时会为每一个 children 创建一个实例。这就意味着当用户在共享一个模板的路由间跳转的时候，将会重新挂载组件实例，重新创建 DOM 元素，不保留状态。 



##### 路由导航

在next中有四种可以实现路由导航：

1. 使用 `Link` 组件

    `link`组件是一个拓展了原生 HTML `` 标签的内置组件，用来实现预获取（prefetching） 和客户端路由导航。 

   ```
   <Link href="/count/about">About</Link>
   ```

   同样也可以使用jsx语法做一个动态渲染，来动态的设置href的值。

2. 使用 `useRouter` Hook（客户端组件）

    客户端组件中用于更改路由的 hook 

   ```tsx
   "use client"
   
   import { useRouter } from 'next/navigation'
    
   export default function Page() {
     const router = useRouter()
    
     return (
       <button type="button" onClick={() => router.push('/count')}>
         count
       </button>
     )
   }
   ```

   

3. 使用 `redirect` 函数（服务端组件）

    服务端组件可以用 redirect 函数来更改路由

   ```tsx
   export default async function Profile({ params }:any) {
     const team = await fetchTeam(params.id)
     if (!team) {
       redirect('/detail')
     }
   }
   ```

   

4. 使用浏览器原生 History API

   使用浏览器原生的 [window.history.pushState](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAPI%2FHistory%2FpushState) 和 [window.history.replaceState](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAPI%2FHistory%2FreplaceState) 方法更新浏览器的历史记录堆栈。通常与 usePathname（获取路径名的 hook） 和 useSearchParams（获取页面参数的 hook） 一起使用。 

   ```tsx
   'use client'
    
   import { useSearchParams } from 'next/navigation'
    
   export default function SortProducts() {
     const searchParams = useSearchParams()
    
     function updateSorting(sortOrder) {
       const params = new URLSearchParams(searchParams.toString())
       params.set('sort', sortOrder)
       window.history.pushState(null, '', `?${params.toString()}`)
     }
    
     return (
       <>
         <button onClick={() => updateSorting('asc')}>Sort Ascending</button>
         <button onClick={() => updateSorting('desc')}>Sort Descending</button>
       </>
     )
   }
   
   ```



##### 动态路由

当业务场景比较复杂时，路由参数在访问时才会确定，这是可以使用动态路由

1. [folderName]

   ```tsx
   interface PageProps {
     params: {
       slug: string;
     };
   }
   
   export default function Page({ params }:PageProps) {
     return <div>My Post: {params.slug}</div>
   }
   ```

   访问`http://localhost:3001/blog/name`，路由中传入的参数就会通过`params.slug`在页面上显示

2. [...folderName]

    方括号内添加省略号，比如 `[...folderName]`，这表示捕获所有后面所有的路由片段。 

   ```tsx
   interface PageProps {
     slug?: string;
     params?:{}
   }
   
   export default function Page({ params }:PageProps) {
     return <div>My Shop: {JSON.stringify(params)}</div>
   }
   ```

   

3. [[...folderName]]

   `[[...folderName]]`，这表示可选的捕获所有后面所有的路由片段。

   这个和上面的唯一区别就是会匹配不带参数的。

   比如`http://localhost:3001/blog1`不会被`app/blog1/[...slug]/page.jsx`匹配到，但是会被`app/blog1/[[...slug]]/page.jsx`匹配



##### 路由处理程序

路由处理程序实际上就是前后端交互的代码，就是request和response。通常定义在`route.js`里，在app目录的嵌套层级下面，不能和page.js同意层级。

比如下面的get请求

```tsx
export async function GET() {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts')
  const data = await res.json()
 
  return NextResponse.json({ data })
}
```

每个请求方法都会被传入两个参数request和 context 。

1. request

    request 对象是一个 [NextRequest](https://juejin.cn/book/7307859898316881957/section/7309079651500949530#heading-23) 对象，它是基于 [Web Request API](https://link.juejin.cn/?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAPI%2FRequest) 的扩展。使用 request ，你可以快捷读取 cookies 和处理 URL。 

2. context

    context 只有一个值就是 `params`，它是一个包含当前动态路由参数的对象。 



##### 中间件

中间件就是用来处理应用里的请求和响应的， 可以基于传入的请求，重写、重定向、修改请求或响应头、甚至直接响应内容。一个比较常见的应用就是鉴权，在打开页面渲染具体的内容前，先判断用户是否登录，如果未登录，则跳转到登录页面。 

###### 设置匹配路径

```tsx
import { NextResponse } from 'next/server'
 
// 中间件可以是 async 函数，如果使用了 await
export function middleware(request) {
  return NextResponse.redirect(new URL('/detail', request.url))
}

// 设置匹配路径
export const config = {
  matcher: '/count/:path*',
}
```

上面这个中间件就是当我们访问到`/count/xx`时会重定向到`/detail`

 `matcher` 不仅支持字符串形式，也支持数组形式，用于匹配多个路径： 

```tsx
export const config = {
  matcher: '/about/:path*',
}
```

实际上也可以通过` request.nextUrl.pathname `来获取具体的路径，通过if-else来编写各种逻辑。

###### 中间件逻辑

 对于传入的请求，NextRequest 提供了 `get`、`getAll`、`set`和 `delete`方法处理 cookies，你也可以用 `has`检查 cookie 或者 `clear`删除所有的 cookies。 

```tsx
import { NextResponse } from 'next/server'
 
export function middleware(request) {
  // 假设传入的请求 header 里 "Cookie:nextjs=fast"
  let cookie = request.cookies.get('nextjs')
  console.log(cookie) // => { name: 'nextjs', value: 'fast', Path: '/' }
  const allCookies = request.cookies.getAll()
  console.log(allCookies) // => [{ name: 'nextjs', value: 'fast' }]
 
  request.cookies.has('nextjs') // => true
  request.cookies.delete('nextjs')
  request.cookies.has('nextjs') // => false
 
  // 设置 cookies
  const response = NextResponse.next()
  response.cookies.set('vercel', 'fast')
  response.cookies.set({
    name: 'vercel',
    value: 'fast',
    path: '/',
  })
  cookie = response.cookies.get('vercel')
  console.log(cookie) // => { name: 'vercel', value: 'fast', Path: '/' }
  
  // 响应 header 为 `Set-Cookie:vercel=fast;path=/test`
  return response
}
```

设置headers

```tsx
// middleware.js 
import { NextResponse } from 'next/server'
 
export function middleware(request) {
  //  clone 请求标头
  const requestHeaders = new Headers(request.headers)
  requestHeaders.set('x-hello-from-middleware1', 'hello')
 
  // 你也可以在 NextResponse.rewrite 中设置请求标头
  const response = NextResponse.next({
    request: {
      // 设置新请求标头
      headers: requestHeaders,
    },
  })
 
  // 设置新响应标头 `x-hello-from-middleware2`
  response.headers.set('x-hello-from-middleware2', 'hello')
  return response
}

```



#### 连接数据库