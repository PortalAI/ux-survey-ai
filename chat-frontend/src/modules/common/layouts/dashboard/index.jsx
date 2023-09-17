import styled from '@emotion/styled';
import { Outlet, useLocation } from 'react-router-dom';
import { CssBaseline, Paper as MuiPaper } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import { spacing } from '@mui/system';
import GlobalStyle from 'modules/common/style/global';
import Navbar from 'modules/common/components/navbar/navbar';

const Root = styled.div`
  display: flex;
  min-height: 100vh;
`;

const AppContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 100%;
`;

const Paper = styled(MuiPaper)(spacing);

const MainContent = styled(Paper)`
  flex: 1;
  background: ${(props) => props.theme.palette.background.default};

  @media all and (-ms-high-contrast: none), (-ms-high-contrast: active) {
    flex: none;
  }

  .MuiPaper-root .MuiPaper-root {
    box-shadow: none;
  }
`;

const DashboardLayout = () => {
  const location = useLocation();
  const theme = useTheme();
  const isLgUp = useMediaQuery(theme.breakpoints.up('lg'));

  return (
    <Root>
      <CssBaseline />
      <GlobalStyle />
      <AppContent>
        { !location.pathname.startsWith("/chat") && <Navbar />}
        <MainContent px={isLgUp ? 12 : 5}>
          <Outlet />
        </MainContent>
      </AppContent>
    </Root>
  );
};

export default DashboardLayout;
