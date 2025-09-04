/*
 * @Author: jinxudong 18751241086@163.com
 * @Date: 2025-08-14 09:58:56
 * @LastEditors: jinxudong 18751241086@163.com
 * @LastEditTime: 2025-08-14 10:03:13
 * @FilePath: \notes\test.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
const node = treeRef.value.getNode(uid) as Node
Object(node.data,obj)
treeRef.value.updateKeyChildren(uid,node.data.children)