import { ThemeProvider } from 'modules/common/contexts/theme-context';
import { Provider } from 'react-redux';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider as MuiThemeProvider } from '@mui/material/styles';
import useTheme from 'modules/common/hooks/use-theme';
import createTheme from 'modules/common/theme';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Router from './routes';
import store from './store';
/**
 * @returns Entry point in the react application. And also register the providers
 */
const App = () => {
  //
  const { theme } = useTheme();
  //
  return (
    <Provider store={store}>
      <BrowserRouter>
        <ThemeProvider>
          <MuiThemeProvider theme={createTheme(theme)}>
            <Router />
            <ToastContainer />
          </MuiThemeProvider>
        </ThemeProvider>
      </BrowserRouter>
    </Provider>
  );
};
//
export default App;
