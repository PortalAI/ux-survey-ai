import axios from 'axios';
import { ENVIRONMENT } from 'config';
//
const axiosConfig = axios.create({
  baseURL: ENVIRONMENT.BACKEND_API,
});
//
export default axiosConfig;
