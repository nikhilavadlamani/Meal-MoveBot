import React, { useState } from 'react';

function ChatBot() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleChat = (e) => {
    e.preventDefault();
    setResponse('This is your personalized response.');
  };

  return (
    <div>
      <h1>Chat with Me</h1>
      <form onSubmit={handleChat}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      <p>{response}</p>
    </div>
  );
}

export default ChatBot;
