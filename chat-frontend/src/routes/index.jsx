import { useRoutes } from 'react-router-dom';
import routes from './router';

/**
 * Register all the route using useRoute hook
 * @returns
 */
const Router = () => useRoutes(routes);
//
export default Router;
