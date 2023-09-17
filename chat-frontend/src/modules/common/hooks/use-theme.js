import { useContext } from 'react';
import { ThemeContext } from 'modules/common/contexts/theme-context';

const useTheme = () => useContext(ThemeContext);

export default useTheme;
