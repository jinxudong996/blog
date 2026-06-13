## 一、环境准备

后端采用`Python + FastApi`，`Redis`和`MySQL`都在云服务器上，通过docker安装的，向外暴露接口实现的远程连接。

##### 服务部署

前面介绍过[fastapi](https://juejin.cn/post/7579887768228085794)的基本语法，但是缺了部署这个环节，在这里补充下。

我的安装环境都是在阿里云的云服务器上，采用的是`pm2`来管理fastapi项目，首先在`centos`上安装相关依赖和环境：

```python
# 1. 更新系统
sudo yum update -y

# 2. 安装 EPEL 源（Python 虚拟环境需要）
sudo yum install -y epel-release

# 3. 安装 Python3 和 pip
sudo yum install -y python3 python3-pip python3-venv python3-wheel

# 确认 Python 安装
python3 -V
pip3 -V

# 4. 安装 Node.js (使用官方源安装最新 LTS)
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs

# 确认 Node 和 npm 安装
node -v
npm -v

# 5. 安装 PM2 全局
sudo npm install -g pm2
pm2 -v

```

准备测试脚本：

首先准备下虚拟环境：

```
python3 -m venv venv

venv\Scripts\activate
```

新建`main.py`

```python
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
import pymysql


app = FastAPI(title="Simple MySQL Query Service")


def get_connection() -> pymysql.connections.Connection:
	"""创建并返回一个 MySQL 连接。"""

	return pymysql.connect(
		host="118.31.xxx",
		port=3307,
		user="root",
		password="xxx",
		database="blog",
		cursorclass=pymysql.cursors.DictCursor,
		charset="utf8mb4",
	)


@app.get("/hello")
async def hello():
	"""返回 你好 + 当前时间（年月日 时分秒）。"""

	now = datetime.now()
	current_time = now.strftime("%Y年%m月%d日 %H:%M:%S")
	return {"message": f"你好，当前时间是：{current_time}"}


@app.get("/student_score")
async def get_student_score(number: str = Query(..., description="学生编号")):
	"""根据 number 查询 blog 库中 student_score 表的 subject 和 score。"""

	try:
		conn = get_connection()
		with conn:
			with conn.cursor() as cursor:
				sql = (
					"SELECT subject, score "
					"FROM student_score "
					"WHERE number = %s"
				)
				cursor.execute(sql, (number,))
				rows = cursor.fetchall()
	except pymysql.MySQLError as exc:  # 数据库连接或执行出错
		detail = (
			exc.args[1]
			if len(exc.args) > 1
			else str(exc)
		)
		raise HTTPException(status_code=500, detail=f"数据库错误: {detail}") from exc

	if not rows:
		raise HTTPException(status_code=404, detail="未找到该 number 对应的成绩")

	return {"number": number, "results": rows}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

```

本地运行下`python mian.py`，然后测试下我们的接口，看来是没问题的。就着手开始部署到线上。

新建`Gunicorn`配置文件`gunicorn_config.py`：

```
bind = "0.0.0.0:8011"          # 对外端口
workers = 2                    # worker 数量，看 CPU 调整
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
```

开始新建项目依赖`requirements.txt`

```
fastapi
uvicorn[standard]
pymysql
```

同时我的`nginx`的代理转发的配置文件，是这样的

```
location /fastapi/query/ {
        proxy_pass http://127.0.0.1:8011/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
```

接下来将项目文件压缩成zip包，拖到服务器的指定目录，运行`unzip query.zip`解压即可。

然后开始安装依赖：

```
首先开启虚拟环境：
python3 -m venv venv
source venv/bin/activate

然后安装依赖
pip install -r requirements.txt

这一步可能安装巨慢，建议切换阿里云的下载链接
```

> 这里巨坑，折腾了我一个多小时，阿里云的python版本默认是3.6.8，使用`Gunicorn`需要3.10以上的，一开始安装依赖一直卡住了，也不报错，换了好几个源，还是不行，我以为我服务器带宽小导致的，换成本地安装，然后拖到服务器上，这才发现是版本的原因，然后安装`3.11.9`后删除虚拟环境，重新安装才成功。

安装成功后，就可以啦。

测试下：运行`gunicorn -c gunicorn_config.py main:app`，在开启一个服务器连接，

```
输入：
curl "http://127.0.0.1:8011/hello"
{"message":"你好，当前时间是：2026年02月08日 15:38:53"}[root@iZbp1f9urggte5qz3ri1riZ ~]# 
curl "http://127.0.0.1:8011/student_score?number=20180101"
{"number":"20180101","results":[{"subject":"母猪的产后护理","score":78},{"subject":"论萨达姆的战争准备","score":88}]}[root@iZbp1f9urg
```

可以看到我们的服务器已经正常运行了，二级域名已经解析了，nginx代理也已经配置了，

输入` curl http://api.jinxudong.com/fastapi/query/hello`可以看到正常的接口输出的，说明我们的脚本已经部署成功了，但是这种部署方式还是比较原始的，而且后续服务肯定不止这个一个，我打算采用`pm2`来管理这些服务。

在项目的根目录写上配置文件`ecosystem.config.js `

```js
module.exports = {
  apps: [
    {
      name: "query",
      script: "bash",
      args: "-c '/var/www/python/query/venv/bin/gunicorn -c gunicorn_config.py main:app'",
      cwd: "/var/www/python/query"
    }
  ]
};

```

运行脚本`pm2 start ecosystem.config.js`就可以看到我们的服务了，在设置下开机自启：

```
pm2 save
pm2 startup
```

我们的服务已经正常部署到线上啦，可以通过域名去访问

```
https://api.jinxudong.com/fastapi/query/student_score?number=20180101

{"number":"20180101","results":[{"subject":"母猪的产后护理","score":78},{"subject":"论萨达姆的战争准备","score":88}]}
```



##### 压测工具介绍

一个系统上线后，是必须要经过压测的，就是模拟大量用户同时访问服务，找到系统的极限QPS，极限并发，找出性能瓶颈，避免线上事故。

接下来介绍两个常见的压测工具：

1. ab

   这是` Apache `自带的压测工具，非常的简轻量，很适合小接口测试，做下简单的性能验证。

   首先安装下这个工具

   ```
   yum install httpd-tools
   ```

   使用也很简单

   ```
   ab -n 1000 -c 50 https://api.jinxudong.com/fastapi/query/student_score?number=20180101
   ```

   用50的并发完成1000次请求，看下ab的输出日志

   ```
   Server Software:        nginx/1.20.1
   Server Hostname:        api.jinxudong.com
   Server Port:            443
   SSL/TLS Protocol:       TLSv1.2,ECDHE-RSA-AES256-GCM-SHA384,2048,256
   Server Temp Key:        X25519 253 bits
   TLS Server Name:        api.jinxudong.com
   
   Document Path:          /fastapi/query/student_score?number=20180101
   Document Length:        133 bytes
   
   Concurrency Level:      50
   Time taken for tests:   17.659 seconds
   Complete requests:      1000
   Failed requests:        0
   Total transferred:      283000 bytes
   HTML transferred:       133000 bytes
   Requests per second:    56.63 [#/sec] (mean)
   Time per request:       882.956 [ms] (mean)
   Time per request:       17.659 [ms] (mean, across all concurrent requests)
   Transfer rate:          15.65 [Kbytes/sec] received
   
   Connection Times (ms)
                 min  mean[+/-sd] median   max
   Connect:       11   56 119.1     13    1471
   Processing:    32  810 212.6    807    1854
   Waiting:       30  810 212.6    806    1854
   Total:         48  866 258.9    828    2290
   
   Percentage of the requests served within a certain time (ms)
     50%    828
     66%    911
     75%    998
     80%   1041
     90%   1195
     95%   1295
     98%   1559
     99%   1798
    100%   2290 (longest request)
   ```

   看下几个核心指标

   1. `Request per second`，也就是常说的QPS，也就是每秒可以处理56个请求

   2. `Time per request`，平均响应时间

      ```
      Time per request:       882.956 [ms] (mean)
      Time per request:       17.659 [ms] (mean, across all concurrent requests)
      ```

      第一个时间单个请求平均耗时，这是用户真实的体验时间，第二个时间是平均耗时/并发数

   3. 延迟分布

      ```
      Percentage of the requests served within a certain time (ms)
        50%    828
        66%    911
        75%    998
        80%   1041
        90%   1195
        95%   1295
        98%   1559
        99%   1798
       100%   2290 (longest request)
      ```

      第一个数字是百分比，第二个是耗时，换成表格是这样

      | 百分位 | 含义             |
      | ------ | ---------------- |
      | P50    | 50%请求 < 828ms  |
      | P90    | 90%请求 < 1195ms |
      | P95    | 95%请求 < 1295ms |
      | P99    | 99%请求 < 1798ms |
      | max    | 最慢请求 2290ms  |

   4. 连接时间分析

      ```
      Connection Times (ms)
                    min  mean[+/-sd] median   max
      Connect:       11   56 119.1     13    1471
      Processing:    32  810 212.6    807    1854
      Waiting:       30  810 212.6    806    1854
      Total:         48  866 258.9    828    2290
      ```

      这里的`Connect`就是`TCP`握手简历链接的时间，`Processing`就是后端处理的时间

2. wrk

wrk目前是后端常用的压测工具，支持多线程和Lua脚本，可以模拟真实并发。

首先在服务器上安装下

```
#先安装编译工具
sudo yum groupinstall "Development Tools" -y
sudo yum install git -y
#下载
curl -L -o wrk.zip https://codeload.github.com/wg/wrk/zip/refs/heads/master
unzip wrk.zip
cd wrk-master

#编译
make

#复制到全局路径
sudo cp wrk /usr/local/bin/
```

安装成功以后，直接测试：

```
wrk -t4 -c100 -d30s --latency https://api.jinxudong.com/fastapi/query/student_score?number=20180101
```

意思就是四个线程，100的并发，测试30秒

```
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.18s    66.72ms   1.42s    96.70%
    Req/Sec    36.35     26.08   100.00     54.00%
  Latency Distribution
     50%    1.18s 
     75%    1.19s 
     90%    1.20s 
     99%    1.23s 
  2483 requests in 30.07s, 698.34KB read
Requests/sec:     82.58
Transfer/sec:     23.22KB
```

可以看到，`Requests/sec`就是吞吐量82，每秒可以处理82个请求，平均延迟1.23秒，

压测还是比较简单的，就是利用工具查看qps和延迟时间，当qps不涨，延迟时间飞涨甚至于报错，那说明就到达极限了。

下面就开始实战环节了。

## 二、信息查询系统

这是一个查询商品信息的系统，就是查询商品详情，为了增加系统的吞吐量，常见的做法就是增加一个缓存层，流程就是：请求接口来了，先去查询redis缓存层，缓存命中就直接返回；如果未命中再去查库。这也是前面介绍的旁路缓存，用内存换取数据库压力。

系统架构图如下

```
客户端 (浏览器/APP)
        |
        v
    FastAPI 接口层
        |
    -----------------
    |               |
Redis 缓存         MySQL 数据库
```



##### 环境准备

数据库设计

```python
CREATE TABLE products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

`id` 是主键

`name`, `price`, `stock`, `description` 是商品核心信息

`updated_at` 商品的更新时间，可以用于后面缓存过期策略（缓存失效时刷新）

然后插入一些测试数据

```
INSERT INTO products (name, price, stock, description)
SELECT
    CONCAT('商品-', t.num),
    ROUND(RAND() * 500 + 10, 2),
    FLOOR(RAND() * 100),
    CONCAT('这是商品 ', t.num, ' 的描述')
FROM (
    SELECT a.n + b.n * 10 + c.n * 100 + 1 AS num
    FROM
        (SELECT 0 n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
         UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a,
        (SELECT 0 n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
         UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b,
        (SELECT 0 n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4
         UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c
) t
WHERE t.num <= 1000;
```

准备工作已经就绪，接下来开始编写代码啦

##### 系统编写

代码也比较简单，就是一个查询接口，和前面是实例基本一致

```python
@app.get("/get_product")
async def get_product(id: int = Query(..., description="商品编号")):
	"""根据商品 id 查询商品信息。"""
	try:
		conn = get_connection()
		with conn:
			with conn.cursor() as cursor:
				sql = (
					"SELECT * "
					"FROM products "
					"WHERE id = %s"
				)
				cursor.execute(sql, (id,))
				rows = cursor.fetchall()
	except pymysql.MySQLError as exc:  # 数据库连接或执行出错
		detail = (
			exc.args[1]
			if len(exc.args) > 1
			else str(exc)
		)
		raise HTTPException(status_code=500, detail=f"数据库错误: {detail}") from exc

	if not rows:
		raise HTTPException(status_code=404, detail="未找到该 id 对应的商品信息")

	return {"id": id, "results": rows}


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

然后运行`python main.py`，`http://localhost:8000/get_product?id=22`是可以看到数据返回的。

说明我们的代码是没问题的，接下来就开始部署，然后再服务器上做压测，看下当前的服务器的最大QPS是多大。

部署方案和前面介绍的一致，记得更改`nginx`配置和`pm2`的配置文件，通过公网访问下我们的接口

```json
https://api.jinxudong.com/fastapi/queryDetail/get_product?id=122
可以看到如下输出：
{
  "id": 122,
  "results": [
    {
      "id": 122,
      "name": "商品-172",
      "price": 461.79,
      "stock": 72,
      "description": "这是商品 172 的描述",
      "updated_at": "2026-02-10T04:13:17"
    }
  ]
}
```

说明接口已经部署成功了，下面就开始压测，要知道这个接口的最大QPS，接下来使用ab来开始压测

###### 第一次压测

首先使用20的并发，看下压测报告：

```
ab -n 1000 -c 20 https://api.jinxudong.com/fastapi/queryDetail/get_product?id=122

压测报告截取：
Requests per second:    54.99 [#/sec] (mean)  
Time per request:       363.704 [ms] (mean)  
50%    307ms
75%    417ms
90%    512ms
99%   1282ms
```

可以看到QPS54，平均时间363ms，延迟分布中50%的请求小于307ms

###### 第二次压测

使用40的并发，看下压测报告：

```
ab -n 1000 -c 40 https://api.jinxudong.com/fastapi/queryDetail/get_product?id=122
 
压测报告截取：
Requests per second:    53.87 [#/sec] (mean)
Time per request:       742.486 [ms] (mean)
  50%    712
  66%    769
  75%    826
  80%    850
  90%    926
```

QPS53，延迟时间和平均请求时间都在增大，有一种步子迈大了的感觉，减少并发试试

###### 第三次压测

使用10的并发，看下压测报告

```
 ab -n 1000 -c 10 https://api.jinxudong.com/fastapi/queryDetail/get_product?id=122
 
 压测报告截取：
 Requests per second:    55.53 [#/sec] (mean)
Time per request:       180.081 [ms] (mean)
  50%    135
  66%    154
  75%    173
  80%    181
  90%    332
```

QPS55，平均时间和延迟时间都降低了，但是QPS确实没怎么变化，可以断定当前系统的最大吞吐量就是55，下面增加一个缓存层，然后看下系统的吞吐量是否发生变化

##### 存增加缓存层

首先回顾下旁路缓存，当查询时首先去缓存中查找，如果缓存命中就直接返回；如果未命中就去查询数据库，然后将值写到缓存中，如果数据库也没有，就写一个空值到缓存中，防止穿透。这就是下面要写的代码的逻辑。

直接看下接口代码

```python
@app.get("/get_product")
async def get_product(id: int = Query(..., description="商品编号")):
	"""根据商品 id 查询商品信息。"""

	cache_key = _make_product_cache_key(id)

	# 1. 先查 Redis 缓存
	try:
		cached = redis_client.get(cache_key)
		if cached is not None:
			rows = json.loads(cached)
			# 缓存命中空列表，说明数据库也没有，直接返回 404，防止缓存穿透
			if not rows:
				raise HTTPException(status_code=404, detail="未找到该 id 对应的商品信息")
			return {"id": id, "results": rows}
	except redis.RedisError:
		# 缓存异常时，降级为直接查数据库
		pass

	try:
		conn = get_connection()
		with conn:
			with conn.cursor() as cursor:
				sql = (
					"SELECT * "
					"FROM products "
					"WHERE id = %s"
				)
				cursor.execute(sql, (id,))
				rows = cursor.fetchall()
	except pymysql.MySQLError as exc:  # 数据库连接或执行出错
		detail = (
			exc.args[1]
			if len(exc.args) > 1
			else str(exc)
		)
		raise HTTPException(status_code=500, detail=f"数据库错误: {detail}") from exc

	if not rows:
		# 数据库未命中，也写入空列表到缓存，防止穿透
		try:
			redis_client.setex(cache_key, 60, json.dumps([]))
		except redis.RedisError:
			pass
		raise HTTPException(status_code=404, detail="未找到该 id 对应的商品信息")

	# 查询到数据后写入缓存
	try:
		encoded_rows = jsonable_encoder(rows)
		redis_client.setex(cache_key, 300, json.dumps(encoded_rows, ensure_ascii=False))
	except (redis.RedisError, TypeError, ValueError):
		# 缓存写入失败不影响接口主流程
		pass

	return {"id": id, "results": rows}

```

首先在接口请求时，一开始就构建了缓存的key，`_make_product_cache_key`的方法是这样的

```python
def _make_product_cache_key(product_id: int) -> str:
	"""生成商品缓存 key。"""

	return f"product:{product_id}"
```

构建的key就是`product:{product_id}`，然后就先查询缓存，如果缓存命中就直接返回，未命中就查库；命中时也有个非空判断，如果是写入的空数组，表明是数据库也没有的，直接返回404，防止穿透。查询数据库就是和前面一样的逻辑了，加了个写入缓存的逻辑：`redis_client.setex(cache_key, 300, json.dumps(encoded_rows, ensure_ascii=False))`。当数据库也没有时，就写个空，防止穿透：`redis_client.setex(cache_key, 60, json.dumps([]))`，然后返回错误。

部署到线上后，`https://api.jinxudong.com/fastapi/queryDetail/get_product?id=5`接口有正常的返回，看下`redis`数据库，也有相关的`product:5`作为key，表明我们的更改是成功的。

要想证明我们的更改效果，就需要做压测了，

###### 第一次压测

直接使用40的并发

```
ab -n 1000 -c 40 https://api.jinxudong.com/fastapi/queryDetail/get_product?id=122

Requests per second: 73.80 [#/sec] (mean) 
Time per request: 542.007 [ms] (mean)
```

我以为这个QPS会变得非常大，才是73，而没加`redis`是53，我查看了`redis`数据库，缓存是存在的，虽然说QPS增加了，但是并不是很明显，看来影响系统的吞吐量的并不只是查询数据库，还有TCP连接，因为这个接口多了一层nginx转发，

###### 第二次压测

这次不走nginx转发了，直接走系统的服务

```
ab -n 1000 -c 40 http://127.0.0.1:8012/get_product?id=122

Requests per second:    365.20 [#/sec] (mean)
Time per request:       109.528 [ms] (mean)
```

QPS一下子就起来了，而且平均响应时间也降低了。

两次测试结果有点出乎意料，都说`redis`毫秒级别的响应，但是QPS并没有指数级别的上升，看来对于小型应用，提升QPS来说，`redis`的作用其实并没有那么大，我的服务器宽带只有2M，费这么大劲，还不如去增加点带宽效果来的明显。

