/* eslint-disable no-param-reassign */
// Accepts the array and key
const groupBy = (array, key) =>
  // Return the end result
  array.reduce((result, currentValue) => {
    // If an array already present for key, push it to the array. Else create an array and push the object
    result[currentValue[key]] = result[currentValue[key]] || [];
    if (currentValue?.readings?.length) {
      result[currentValue[key]].push(currentValue?.readings[0]);
    }
    // Return the current iteration `result` value, this will be taken as next iteration `result` value and accumulate
    return result;
  }, {}); // empty object is the initial value for result object
//
export default groupBy;
