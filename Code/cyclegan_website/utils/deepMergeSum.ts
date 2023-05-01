export const deepMergeSum = (obj1: any, obj2: any) => {
  return Object.keys(obj1).reduce((acc: any, key: any) => {
    if (typeof obj2[key] === "object") {
      acc[key] = deepMergeSum(obj1[key], obj2[key]);
    } else if (obj2.hasOwnProperty(key) && !isNaN(parseFloat(obj2[key]))) {
      acc[key] = obj1[key] + obj2[key];
    }
    return acc;
  }, {});
};
