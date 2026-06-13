##### 

###### 1、可回收且低脂的产品

> ```
> +-------------+---------+
> | Column Name | Type    |
> +-------------+---------+
> | product_id  | int     |
> | low_fats    | enum    |
> | recyclable  | enum    |
> +-------------+---------+
> product_id 是该表的主键（具有唯一值的列）。
> low_fats 是枚举类型，取值为以下两种 ('Y', 'N')，其中 'Y' 表示该产品是低脂产品，'N' 表示不是低脂产品。
> recyclable 是枚举类型，取值为以下两种 ('Y', 'N')，其中 'Y' 表示该产品可回收，而 'N' 表示不可回收。
> 编写解决方案找出既是低脂又是可回收的产品编号。
> ```

这个就比较简单了，简单的查询

`SELECT product_id  FROM Products WHERE low_fats = 'Y' AND recyclable = 'Y'`

###### 2、寻找用户推荐人

> ```
> +-------------+---------+
> | Column Name | Type    |
> +-------------+---------+
> | id          | int     |
> | name        | varchar |
> | referee_id  | int     |
> +-------------+---------+
> 在 SQL 中，id 是该表的主键列。
> 该表的每一行表示一个客户的 id、姓名以及推荐他们的客户的 id。
> ```
>
> 找出以下客户的姓名：
>
> 1. **被任何** `id != 2` 的用户推荐。
> 2. **没有被** 任何用户推荐。

这里主要就是考察判断`NULL`的方法

```sql
SELECT name
FROM Customer
WHERE referee_id != 2 OR referee_id IS NULL;
```



###### 3、大的国家

> ```
> +-------------+---------+
> | Column Name | Type    |
> +-------------+---------+
> | name        | varchar |
> | continent   | varchar |
> | area        | int     |
> | population  | int     |
> | gdp         | bigint  |
> +-------------+---------+
> name 是该表的主键（具有唯一值的列）。
> 这张表的每一行提供：国家名称、所属大陆、面积、人口和 GDP 值。
> ```
>
>  
>
> 如果一个国家满足下述两个条件之一，则认为该国是 **大国** ：
>
> - 面积至少为 300 万平方公里（即，`3000000 km2`），或者
> - 人口至少为 2500 万（即 `25000000`）
>
> 编写解决方案找出 **大国** 的国家名称、人口和面积。

```sql
SELECT name,population ,area FROM World WHERE  area >= 3000000 OR population >= 25000000
```



###### 3、文章浏览

> ```
> +---------------+---------+
> | Column Name   | Type    |
> +---------------+---------+
> | article_id    | int     |
> | author_id     | int     |
> | viewer_id     | int     |
> | view_date     | date    |
> +---------------+---------+
> 此表可能会存在重复行。（换句话说，在 SQL 中这个表没有主键）
> 此表的每一行都表示某人在某天浏览了某位作者的某篇文章。
> 请注意，同一人的 author_id 和 viewer_id 是相同的。
> ```
>
>  
>
> 请查询出所有浏览过自己文章的作者。
>
> 结果按照作者的 `id` 升序排列。

这个题难点其实是题目阅读，就是找出自己阅读过的文章，然后排序去重

```
SELECT DISTINCT author_id AS ID FROM Views WHERE  author_id  = viewer_id  ORDER BY author_id
```

```
SELECT author_id AS ID FROM Views WHERE  author_id  = viewer_id   GROUP BY author_id ORDER BY author_id
```



##### 5、无效的推文

> ```
> +----------------+---------+
> | Column Name    | Type    |
> +----------------+---------+
> | tweet_id       | int     |
> | content        | varchar |
> +----------------+---------+
> 在 SQL 中，tweet_id 是这个表的主键。
> content 只包含字母数字字符，'!'，' '，不包含其它特殊字符。
> 这个表包含某社交媒体 App 中所有的推文。
> ```
>
>  
>
> 查询所有无效推文的编号（ID）。当推文内容中的字符数**严格大于** `15` 时，该推文是无效的。

这个也简单，知道统计字符的方法就行了

```
SELECT tweet_id FROM Tweets WHERE LENGTH(content) > 15
```



###### 6、使用唯一标识码替换员工ID

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| name          | varchar |
+---------------+---------+
在 SQL 中，id 是这张表的主键。
这张表的每一行分别代表了某公司其中一位员工的名字和 ID 。
 

EmployeeUNI 表：

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| unique_id     | int     |
+---------------+---------+
在 SQL 中，(id, unique_id) 是这张表的主键。
这张表的每一行包含了该公司某位员工的 ID 和他的唯一标识码（unique ID）。
 

展示每位用户的 唯一标识码（unique ID ）；如果某位员工没有唯一标识码，使用 null 填充即可。
```

这道题目主要考察的是`join`的用法，一般来说常用的就两种

1. INNER JOIN

   join语法的骨架是这样的，`SELECT 列 FROM 表A [JOIN_TYPE] 表B ON 连接条件 [WHERE 过滤条件]`

   而`JOIN_TYPE`是`INNER JOIN`时，表明取A和B的公共部分，也就是两个表必须都匹配，不匹配的直接消失

2. LEFT JOIN

   当`JOIN_TYPE`是`LEFT JOIN`时，就是以左表为准，右表能匹配就匹配，匹配不上就时NULL。

所以这道题目考察的就是`LEFT JOIN`的用法

`SELECT a.name,b.unique_id FROM Employees a LEFT JOIN EmployeeUNI b ON a.id = b.id`

###### 7、产品销售分析

销售表 `Sales`

```
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
(sale_id, year) 是销售表 Sales 的主键（具有唯一值的列的组合）。
product_id 是关联到产品表 Product 的外键（reference 列）。
该表的每一行显示 product_id 在某一年的销售情况。
注意: price 表示每单位价格。
```

产品表 `Product`：

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
+--------------+---------+
product_id 是表的主键（具有唯一值的列）。
该表的每一行表示每种产品的产品名称。
```



编写解决方案，以获取 `Sales` 表中所有 `sale_id` 对应的 `product_name` 以及该产品的所有 `year` 和 `price` 

和6一样

`SELECT b.product_name ,a.year,a.price FROM Sales a LEFT JOIN Product b ON a.product_id = b.product_id`

###### 8、进店却未进行过交易的顾客

表：`Visits`

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| visit_id    | int     |
| customer_id | int     |
+-------------+---------+
visit_id 是该表中具有唯一值的列。
该表包含有关光临过购物中心的顾客的信息。
```

表：`Transactions`

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| transaction_id | int     |
| visit_id       | int     |
| amount         | int     |
+----------------+---------+
transaction_id 是该表中具有唯一值的列。
此表包含 visit_id 期间进行的交易的信息。
```

 

有一些顾客可能光顾了购物中心但没有进行交易。请你编写一个解决方案，来查找这些顾客的 ID ，以及他们只光顾不交易的次数。

```sql
SELECT
    v.customer_id,
    COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t
    ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;
```

###### 9、上升的温度

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| recordDate    | date    |
| temperature   | int     |
+---------------+---------+
id 是该表具有唯一值的列。
没有具有相同 recordDate 的不同行。
该表包含特定日期的温度信息
```

编写解决方案，找出与之前（昨天的）日期相比温度更高的所有日期的 `id` 。

```sql
SELECT w1.id
FROM Weather w1
JOIN Weather w2
  ON w1.recordDate = DATE_ADD(w2.recordDate, INTERVAL 1 DAY)
WHERE w1.temperature > w2.temperature;
```

还可以使用窗口函数：

```sql
SELECT id
FROM (
    SELECT id,
           temperature,
           LAG(temperature) OVER (ORDER BY recordDate) AS prev_temp
    FROM Weather
) t
WHERE temperature > prev_temp;
```

###### 10、每台机器的进程平均运行时间

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| machine_id     | int     |
| process_id     | int     |
| activity_type  | enum    |
| timestamp      | float   |
+----------------+---------+
该表展示了一家工厂网站的用户活动。
(machine_id, process_id, activity_type) 是当前表的主键（具有唯一值的列的组合）。
machine_id 是一台机器的ID号。
process_id 是运行在各机器上的进程ID号。
activity_type 是枚举类型 ('start', 'end')。
timestamp 是浮点类型,代表当前时间(以秒为单位)。
'start' 代表该进程在这台机器上的开始运行时间戳 , 'end' 代表该进程在这台机器上的终止运行时间戳。
同一台机器，同一个进程都有一对开始时间戳和结束时间戳，而且开始时间戳永远在结束时间戳前面。
```

现在有一个工厂网站由几台机器运行，每台机器上运行着 **相同数量的进程** 。编写解决方案，计算每台机器各自完成一个进程任务的平均耗时。

完成一个进程任务的时间指进程的`'end' 时间戳` 减去 `'start' 时间戳`。平均耗时通过计算每台机器上所有进程任务的总耗费时间除以机器上的总进程数量获得。

结果表必须包含`machine_id（机器ID）` 和对应的 **average time（平均耗时）** 别名 `processing_time`，且**四舍五入保留3位小数。**

以 **任意顺序** 返回表。

```sql
SELECT
    machine_id,
    ROUND(AVG(end_time - start_time), 3) AS processing_time
FROM (
    SELECT
        machine_id,
        process_id,
        MAX(CASE WHEN activity_type = 'start' THEN timestamp END) AS start_time,
        MAX(CASE WHEN activity_type = 'end' THEN timestamp END) AS end_time
    FROM Activity
    GROUP BY machine_id, process_id
) AS t
GROUP BY machine_id;
```



###### 11、员工奖金

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| empId       | int     |
| name        | varchar |
| supervisor  | int     |
| salary      | int     |
+-------------+---------+
empId 是该表中具有唯一值的列。
该表的每一行都表示员工的 id 和姓名，以及他们经理的 id 和他们的工资。
```

 

表：`Bonus`

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| empId       | int  |
| bonus       | int  |
+-------------+------+
empId 是该表具有唯一值的列。
empId 是 Employee 表中 empId 的外键(reference 列)。
该表的每一行都包含一个员工的 id 和他们各自的奖金。
```

 

编写一个解决方案来报告满足以下任一条件的每个员工的姓名和奖金金额：

- 奖金 **少于** `1000` 的员工。
- 没有任何奖金的员工。

和前面一样，就是join的用法

`SELECT W1.name,W2.bonus FROM Employee W1 LEFT JOIN Bonus W2 ON W1.empId = W2.empId WHERE (W2.Bonus IS NULL OR W2.Bonus < 1000 )`

###### 12、学生们参加各科测试的次数

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| student_id    | int     |
| student_name  | varchar |
+---------------+---------+
在 SQL 中，主键为 student_id（学生ID）。
该表内的每一行都记录有学校一名学生的信息。
```

 

科目表: `Subjects`

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| subject_name | varchar |
+--------------+---------+
在 SQL 中，主键为 subject_name（科目名称）。
每一行记录学校的一门科目名称。
```

 

考试表: `Examinations`

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| subject_name | varchar |
+--------------+---------+
这个表可能包含重复数据（换句话说，在 SQL 中，这个表没有主键）。
学生表里的一个学生修读科目表里的每一门科目。
这张考试表的每一行记录就表示学生表里的某个学生参加了一次科目表里某门科目的测试。
```

查询出每个学生参加每一门科目测试的次数，结果按 `student_id` 和 `subject_name` 排序。

```sql
SELECT
    S.student_id,
    S.student_name,
    Sub.subject_name,
    COUNT(E.subject_name) AS attended_exams
FROM Students S
CROSS JOIN Subjects Sub   -- 每个学生对应每门科目
LEFT JOIN Examinations E
    ON S.student_id = E.student_id AND Sub.subject_name = E.subject_name
GROUP BY
    S.student_id,
    S.student_name,
    Sub.subject_name
ORDER BY
    S.student_id,
    Sub.subject_name;

```

###### 13、至少有5名直接下属的经理

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id 是此表的主键（具有唯一值的列）。
该表的每一行表示雇员的名字、他们的部门和他们的经理的id。
如果managerId为空，则该员工没有经理。
没有员工会成为自己的管理者
```



###### 确认率

###### 有趣的电影

```
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| id             | int      |
| movie          | varchar  |
| description    | varchar  |
| rating         | float    |
+----------------+----------+
id 是该表的主键(具有唯一值的列)。
每行包含有关电影名称、类型和评级的信息。
评级为 [0,10] 范围内的小数点后 2 位浮点数。
```

`SELECT * FROM cinema WHERE description != 'boring' AND id % 2 = 1 ORDER BY rating DESC`

###### 平均售价

表：`Prices`

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| start_date    | date    |
| end_date      | date    |
| price         | int     |
+---------------+---------+
(product_id，start_date，end_date) 是 prices 表的主键（具有唯一值的列的组合）。
prices 表的每一行表示的是某个产品在一段时期内的价格。
每个产品的对应时间段是不会重叠的，这也意味着同一个产品的价格时段不会出现交叉。
```

表：`UnitsSold`

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| purchase_date | date    |
| units         | int     |
+---------------+---------+
该表可能包含重复数据。
该表的每一行表示的是每种产品的出售日期，单位和产品 id。
```

 

编写解决方案以查找每种产品的平均售价。`average_price` 应该 **四舍五入到小数点后两位**。如果产品没有任何售出，则假设其平均售价为 0。

```
SELECT
  p.product_id,
  ROUND(
    COALESCE(SUM(p.price * u.units) / SUM(u.units), 0),
    2
  ) AS average_price
FROM Prices p
LEFT JOIN UnitsSold u
  ON p.product_id = u.product_id
 AND u.purchase_date BETWEEN p.start_date AND p.end_date
GROUP BY p.product_id;

```



###### 项目员工

###### 各赛事的用户注册率

###### 查询结果和质量占比

###### 每月交易

###### 即时食物配送

###### 游戏玩法分析

###### 每位教师所传授的科目种类数量

###### 查询近30天活跃用户数

###### 销售分析

###### 超过5名学生的课

###### 求关注者的数量

###### 只出现一次的最大数字

###### 买下所有产品的客户

###### 每位经理的下属员工数量

###### 员工的直属部门

###### 判断三角形

###### 连续出现的数字

###### 指定日期的产品价格

###### 最后一个能进入巴士的人

