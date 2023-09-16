import { useState, useEffect, useRef } from 'react';

const useWebSocket = (url) => {
  const [messages, setMessages] = useState([]);
  const ws = useRef(null);

  useEffect(() => {

    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log("Connected to the WebSocket server");
    };

    ws.current.onmessage = (event) => {
      const messageData = JSON.parse(event.data);
      setMessages((prev) => [...prev, messageData]);
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket Error:", error);
    };

    ws.current.onclose = (event) => {
      if (event.wasClean) {
        console.log(`Closed clean, code=${event.code}, reason=${event.reason}`);
      } else {
        console.warn('Connection died');
      }
    };

    // return () => {
    //   ws.current.close();
    //   console.log("Disconnected from the WebSocket server");
    // };

  }, [url]);

  const sendMessage = (currentMessage) => {

    if (currentMessage.trim() !== '' && ws && ws.readyState === WebSocket.OPEN) {
      setMessages(prev => [...prev, currentMessage]);
      console.log(`prepare to send message ${messages}`)
      ws.send(currentMessage);
    }
  };

  return [messages, sendMessage];
};

export default useWebSocket;
