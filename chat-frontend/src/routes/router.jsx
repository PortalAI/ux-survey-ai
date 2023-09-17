import ROUTES from 'modules/common/constants/route';
import DashboardLayout from 'modules/common/layouts/dashboard';
import { BusinessInfoView } from 'modules/business-info/components';
import { Page404 } from 'modules/error-pages';
import { PresentationView } from 'modules/presentation/components';
import { ChatView } from 'modules/chat/components';

/**
 * Define the routeing structure using array. Here include the nested routeing as well.
 * And also define the auth wrapper and private routers for helping to role based routes
 */
const routes = [
  {
    path: ROUTES.ROOT,
    element: <DashboardLayout />,
    children: [
      {
        path: '',
        element: <BusinessInfoView />,
      },
    ],
  },
  {
    path: ROUTES.BUSINESS_INFO,
    element: <DashboardLayout />,
    children: [
      {
        path: '',
        element: <BusinessInfoView />,
      },
    ],
  },
  {
    path: ROUTES.CHAT,
    element: <DashboardLayout />,
    children: [
      {
        path: '',
        element: <ChatView />,
      },
    ],
  },
  {
    path: ROUTES.PRESENTATION,
    element: <DashboardLayout />,
    children: [
      {
        path: '',
        element: <PresentationView />,
      },
    ],
  },
  {
    path: ROUTES.NOT_FOUND,
    element: <Page404 />,
  },
];
//
export default routes;
