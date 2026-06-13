前端人的MySQL笔记

一、基础认识

数据库是一个以某种 有组织的方式存储的数据集合。理解数据库的一种最简单的办法是将其 想象为一个文件柜。此文件柜是一个存放数据的物理位置，不管数据是 什么以及如何组织的 。

而表就是某种特定类型数据的结构化清单，关键在意表中的数据要是同一种类型的数据或者是一个清单。 表具有一些特性，这些特性定义了数据在表中如何存储，如可以存 储什么样的数据，数据如何分解，各部分信息如何命名，等等，描述表 的这组信息就是所谓的模式(schema)

表由列组成，列就是表中的一个字段，所有的表都是由一个或者多个列组成的。列中的数据都有相应的数据类型，类型就代表了可以存储的数据的种类。表中的数据都是按行存储，每一行都是对应具体的记录。而每一行都有一个主键，就是我们可以从众多数据中找到这行数据的唯一标识，比如用户ID。

 SQL（发音为字母S-Q-L或sequel）是结构化查询语言（Structured Query Language）的缩写。SQL是一种专门用来与数据库通信的语言 ，比如常见的`SELECT * FROM TABLES`，就是我们常说的增删查改。



二、数据库与表的基本操作

安装MySQL、连接MySQL其实都很常见，一搜一大把，这里就不描述了。我的做法是，在云服务器上，通过docker安装一个mysql，然后开启长连接，将其作为一个远程数据库访问，在通过`Navicat Permium`远程连接访问就行了。

1. ###### 选择数据库

   查看数据库 `SHOW DATABASES;`

   选择数据库`USE TEXT;`

   查看库中的所有的表`SHOW TABLES`

   显示表的基本结构`SHOW COLUMNS FROM tickets_stock;`

2. ###### 检索数据

   检索数据也就是查询，常见的关键字`SELECT`

   比如查询表中的某一列：`SELECT number FROM `student_score`

   查询多个列：`SELECT number,score FROM student_score;`

   虽然MySQL对于大小写不敏感，也就是`SELECT`和`select`都是一样的，但是有一个约定俗成：对于表名和列名都是小写，其他的语句都是大写的。

   如果想要查询所有的列，最简单的就是使用通配符：`SELECT * FROM student_score`

   查询的数据，要简单的过滤下重复，可以通过`DISYINCT`关键字`SELECT DISTINCT score FROM student_score`

   如果想要查询指定行，可以通过`limit`关键字，比如要查询前五行：`SELECT  score FROM student_score LIMIT 5;`，如果要查询两行，从第五行开始，可以这么做：`SELECT  score FROM student_score LIMIT 5,2;`

   

3. ###### 排序

   排序可以根据`ORDER`关键字，比如下面这句：

   ` SELECT * FROM student_info ORDER BY name  `， 根据名字在`ASC`中的顺序升序排列，

   如果想要根据多个列去排列，可以在后面继续添加`SELECT * FROM student_score ORDER BY score,number;`，这句的意思就是先根据score排列，然后在此基础上再根据number去排列。

   上面的都是升序排列，如果想要降序，在语句后面加个关键字`DESC`就行了

   比如这样：`SELECT * FROM student_score ORDER BY score DESC;`

   如果涉及到多个列的话，关键字`DESC`就要紧跟着对应的列名：

   `SELECT * FROM student_score ORDER BY score DESC,number;`，比如这个语句，就是先根据`score`降序，然后在此基础上再根据`number`升序排列。

   `DESC`关键字可以配合`LIMIT`找到一列中的最大值或者最小值，比如找到成绩最高的同学：

   `SELECT * FROM student_score ORDER BY score DESC LIMIT 1;`

4. ###### 过滤数据

   在检索的时候，如果想查找指定条件的数据，就需要用到`WHERE`关键字，这个也称为过滤

   比如找到成绩及格的学生：

   `SELECT * FROM student_score WHERE score > 60;`

   比如找到表中所有的男生：

   ` SELECT * FROM `student_info` WHERE sex = '男' `，值得一提的是，汉字必须加引号，因为他是字符串，如果不加引号就会被认为是列名，导致报错。

   如果我想找到一个范围，就需要用到`BETWEEN`，比如我想找到成绩在60到80之间的

   `SELECT * FROM student_score WHERE score BETWEEN 60 AND 80;`

   

5. ###### 数据过滤

   实际上`WHERE`关键字还可以组合操作符写出更加复杂的功能，

   比如我想找出计算机学院中的男生

   `SELECT * FROM `student_info` WHERE sex = '男' AND department = '计算机学院'`

   如果上面的`AND`改成`OR`是啥意思呢，

   `SELECT * FROM `student_info` WHERE sex = '男' OR department = '计算机学院'`，`OR`就变成了匹配男生或者计算机学院的

   还有`IN`操作符，`SELECT * FROM `student_score` WHERE score IN (61,78,100)`，匹配出成绩为61,78和100的

   如果上面的`IN`操作符想取反，还有`NOT IN`

   `SELECT * FROM `student_score` WHERE score NOT IN (61,78,100)`

6. 模糊匹配

   上面的匹配条件都是精准的，比如大于小于，如果遇到没有精准的匹配条件的，就需要用到`LIKE`关键字，比如搜索所有姓杜的

   `SELECT * FROM `student_info` WHERE name LIKE '杜%'`

   这里的`%`意思就是任何字符出现的任何次数，而`杜%`就表明以杜开头的字符串，`%杜%`就表明含杜的字符串

   还有一个很有用的字符串`_`，只匹配任意字符串出现一次

   `SELECT * FROM `student_score` WHERE score LIKE '7_'`就是查询成绩7开头的两位数

   

7. 函数

   当我们需要对查询出来的数据做一些简单的处理，就需要用到SQL中的函数，接了来统计下：

   1. 文本处理函数

      `Upper()`将文本转化为大写

      `SELECT *, UPPER(nick_name) AS nick_name_upper FROM student_info;` 这里将`nick_name`这一列转化为大写，并且起了个别名

      当然还有好几个，这里列举下：

      `Length()`：返回字符串的长度

      `Lower()`：将字符串转化为小写

      

   2. 日期和时间处理函数

      处理日期也内置了很多方法

      `Date()`：返回日期时间的日期部分

      `CurDate()`：返回当前日期

      `CurTime()`：返回当前时间

      `Day()`：返回天数

      `Year()`：返回年份

      `Month()`：返回月份

      需要注意的是，在MySQL使用日期格式，无论插入、更新，都需要使用yyyy-mm-dd。

      如果我要查询9.12号至9.30之间的学生信息，可以使用`BETWEEN`关键字

      `SELECT * FROM student_info WHERE enrollment_time BETWEEN '2018-09-12' AND '2018-09-30'`

      

   3. 数值处理函数

      SQL在数值处理，大多都是几何运算，也比较简单其实，简单的列举下

      `Abs()`：返回绝对值

      `Mod()`:  返回余数

      `Rand()`: 返回随机数

8. 汇总数据

    当需要对表中的数据做一些汇总，比如找出指定列的最大值，表中的行数，就需要五个聚集函数

   1. `AVG()`

      返回某列的平均值

      `SELECT AVG(score) AS score_avg FROM student_score`获取平均成绩

      

   2. `MAX()`

      返回指定列的最大值

      `SELECT MAX(score) AS max_score from  student_score`

   3. `COUNT()`

      返回某列的行数

      我要统计表中所有的行数，比如包括空值和NULL

      `SELECT COUNT(*) as count from student_info`

   4. `MIN()`

      `SELECT MIN(score) AS max_score from  student_score`

   5. `SUM()`

      `SELECT SUM(score) AS max_score from  student_score`

9. 分组数据

   分组就是将表中的数据划分为多个逻辑组，对于这个逻辑组单独做运算，就需要用到`GROUP BY`关键字

   比如我要查询男生和女生的平均成绩，就需要将数据根据sex分组

   `SELECT sex, AVG(score) AS score_avg FROM student_score GROUP BY sex`

   如果需要过滤分组的话，就需要使用到`HAVING`关键字，

   比如我要找出平均分超出70 的男生，可以这么做

   `SELECT sex,COUNT(*) as total_count, avg(score) as score_avg FROM student_score GROUP BY sex HAVING AVG(score) >70`

10. 子查询

    子查询就是在select语句中嵌套查询语句，比如我要查询成绩最高的学生的学院

    ```sql
    SELECT department FROM student_info WHERE number = (SELECT number FROM student_score  ORDER BY score DESC LIMIT 1)
    ```

    这个查询是由内而外的，先查询内部的学生编号，然后再去匹配学院

11.  联结表

    

12. 创建高级连结

13. 组合查询

14. 全文本搜索

    



三、数据的增删查改



四、函数与表达式





五、多表查询与JOIN





六、子查询





七、视图





八、安全与权限





九、数据导入与到处





十、性能与优化







































