import React, { useState } from 'react';
import axios from 'axios';

function BusinessLog() {
  const [info, setInfo] = useState("");
  const [links, setLinks] = useState([]);

  const handleSubmit = async () => {
    const response = await axios.post('YOUR_FASTAPI_ENDPOINT/log-business', { info });
    setLinks(response.data.links); // Assuming the API returns a list of links.
  };

  return (
    <div>
      <input 
        type="text" 
        value={info} 
        onChange={(e) => setInfo(e.target.value)} 
        placeholder="Enter business info" 
      />
      <button onClick={handleSubmit}>Submit</button>
      <div>
        {links.map((link, index) => <p key={index}>{link}</p>)}
      </div>
    </div>
  );
}

export default BusinessLog;
