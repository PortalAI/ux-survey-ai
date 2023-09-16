import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import './App.css';
import MyProvider from './state/provider';

import BusinessLog from './components/BusinessLog/BusinessLog';
import ChatUI from './components/ChatUI/ChatUI';


function App() {
  return (
    <MyProvider>
      <Router>
        <div className="App">
          <nav>
            <Link to="/business">Business Log</Link>
            <Link to="/chat">Chat UI</Link>
          </nav>
          <Routes>
            <Route path="/business" element={<BusinessLog />} />
            <Route path="/chat/:survey_id" element={<ChatUI />} />
          </Routes>
        </div>
      </Router>
    </MyProvider>
  );
}

export default App;
