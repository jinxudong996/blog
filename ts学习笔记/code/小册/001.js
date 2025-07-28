var threeSum = function (nums) {
  let left = 0;
  let right = left + 1;
  let right_1 = right + 1;
  let result = [];
  while (right < nums.length - 1) {
    let sum = nums[left] + nums[right];
    for (let i = right_1; i < nums.length; i++) {
      if (nums[i] + sum === 0) {
        result.push([nums[left], nums[right], nums[i]]);
      }
    }
    left++;
    right++;
  }
  return result;
};
threeSum([3, -2, 1, 0]);
// function removeDuplicates(arr) {
//   let sortArr = arr.map((item) => item.sort((a, b) => a - b));

//   return new Set(sortArr);
// }

// console.log(
//   removeDuplicates([
//     [-1, 0, 1],
//     [0, 1, -1],
//     [2, -1, -1],
//   ])
// );
