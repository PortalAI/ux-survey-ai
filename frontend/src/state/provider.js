import React, { useState } from 'react';
import MyContext from './context';

function MyProvider({ children }) {
  const [globalState, setGlobalState] = useState({
    survey_id: null,
    // ... other state data
  });

  return (
    <MyContext.Provider value={[globalState, setGlobalState]}>
      {children}
    </MyContext.Provider>
  );
}

export default MyProvider;
