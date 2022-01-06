class List {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
  find(target) {
    let cur = this;
    while (cur.val !== target) {
      cur = cur.next;
      if (!cur) {
        return false
      }
    }
    return cur
  }

  add(node, target) {
    let newNode = new List(node);
    let cur = this.find(target);
    newNode.next = cur.next;
    cur.next = newNode
  }

  findPre(target) {
    if (!this.find(target)) {
      return false;
    }
    let cur = this;
    while (cur.next.val !== target) {
      cur = cur.next
    }
    return cur;
  }

  // delete(target){
  // 	let deleteNode = this.find(target);
  //        this.findPre(deleteNode.val).next = deleteNode.next
  // }
  delete(target) {
    let deleteNode = this.find(target);
    this.findPre(deleteNode.val).next = deleteNode.next
  }
}
let list = new List('老大')
list.add('老二', '老大')
list.add('老三', '老二')
// list.add('老四', '老三')

console.log(list)


//反转链表
var reverseList = function(head) {
  if (head == null || head.next == null) {
      return head;
  }
  const newHead = reverseList(head.next);
  head.next.next = head;
  head.next = null;
  return newHead;
};


console.log(reverseList(list))
