/* eslint-disable react/jsx-no-constructed-context-values */
/* eslint-disable no-shadow */
/* eslint-disable no-unused-vars */
import THEMES from 'modules/common/constants/themes';
import { createContext, useEffect, useState } from 'react';

const initialState = {
  theme: THEMES.DEFAULT,
  setTheme: (theme) => {},
};

const ThemeContext = createContext(initialState);

function ThemeProvider({ children }) {
  const [theme, _setTheme] = useState(initialState.theme);

  useEffect(() => {
    const storedTheme = localStorage.getItem('theme');

    if (storedTheme) {
      _setTheme(JSON.parse(storedTheme));
    }
  }, []);

  const setTheme = (theme) => {
    localStorage.setItem('theme', JSON.stringify(theme));
    _setTheme(theme);
  };

  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}

export { ThemeProvider, ThemeContext };
