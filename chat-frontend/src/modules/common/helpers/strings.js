/* eslint-disable import/prefer-default-export */
/* eslint-disable no-unsafe-optional-chaining */
/**
 * Capitalize the first letter of the word
 * @param {*} str
 * @returns
 */
export const capitalizeFirst = (str) => str?.charAt(0).toUpperCase() + str?.slice(1).toLowerCase();
