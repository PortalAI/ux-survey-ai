import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chat from './routes/Chat'; // Assuming you've placed the Chat component in a 'routes' folder

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/chat" element={<Chat />} />
          {/* Add other routes as needed */}
          {/* Example: <Route path="/welcome" element={<Welcome />} /> */}
          {/* Example: <Route path="/summary" element={<Summary />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
