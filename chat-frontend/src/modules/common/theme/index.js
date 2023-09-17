/* eslint-disable prefer-destructuring */
import '@mui/lab/themeAugmentation';

import { createTheme as createMuiTheme } from '@mui/material/styles';
import variants from './variants';
import typography from './typography';
import breakpoints from './breakpoints';
import components from './components';
import shadows from './shadows';

const createTheme = (name) => {
  let themeConfig = variants.find((variant) => variant.name === name);

  if (!themeConfig) {
    themeConfig = variants[0];
  }

  return createMuiTheme(
    {
      spacing: 4,
      breakpoints,
      components,
      typography,
      shadows,
      palette: themeConfig.palette,
    },
    {
      name: themeConfig.name,
      header: themeConfig.header,
      footer: themeConfig.footer,
      sidebar: themeConfig.sidebar,
    }
  );
};

export default createTheme;
