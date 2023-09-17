/* eslint-disable import/no-cycle */
import axios from './axios';

export class ResponseError extends Error {
  constructor(error) {
    super(`${error.code} - ${error.message}`);
  }
}
/**
 * Parses the JSON returned by a network request
 *
 * @param  {object} response A response from a network request
 *
 * @return {object} The parsed JSON from the request
 */
const parseJSON = (response) => {
  if (response.status === 204 || response.status === 205) {
    return null;
  }
  return response.data;
};
/**
 * Checks if a network request came back fine, and throws an error if not
 *
 * @param  {object} response   A response from a network request
 *
 * @return {object|undefined} Returns either the response, or throws an error
 */
const errorHandling = async (error) => {
  const errorResponse = new ResponseError(error);
  errorResponse.message = error.response.data;
  throw errorResponse;
};
/**
 * Requests a URL, returning a promise
 *
 * @param  {string} url       The URL we want to request
 * @param  {object} [options] The options we want to pass to "fetch"
 * @param  {boolean} multipart Multipart request
 * @return {object}           The response data
 */
const request = async (_metadata, data, isSecure = true, multipart = false) => {
  const payload = { ...data };
  const metadata = { ..._metadata };
  const pathTokens = metadata.path.split(':');
  //
  if (metadata.path.indexOf(':') !== 0) {
    pathTokens.shift();
  }
  //
  pathTokens.forEach((token) => {
    if (token.includes('/')) {
      const key = token.split('/')[0];
      metadata.path = metadata.path.replace(`:${key}`, `${payload[key]}`);
      delete payload[key];
    } else {
      metadata.path = metadata.path.replace(`:${token}`, `${payload[token]}`);
      delete payload[token];
    }
  });
  let requestBody = JSON.stringify(payload);
  if (multipart) {
    const formData = new FormData();
    formData.append('file', payload.file);
    requestBody = formData;
  }
  const options = {
    method: metadata.method,
    // mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache',
    url: metadata.path,
    // credentials: 'include', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      ...(isSecure && {
        Authorization: '',
      }),
      ...(multipart && {
        enctype: 'multipart/form-data',
      }),
    },
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // no-referrer, *client
    ...(['POST', 'PUT', 'PATCH'].includes(metadata.method) && {
      data: requestBody,
    }),
  };
  //
  try {
    const response = await axios(options);
    return parseJSON(response);
  } catch (error) {
    return errorHandling(error);
  }
};
//
export default request;
