import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [sessionId] = useState(generateSessionId());
  const [showInitialMessage, setShowInitialMessage] = useState(true); // State for initial message
  const [isLoading, setIsLoading] = useState(false); // State for loading animation
  const chatBoxRef = useRef(null); // Reference to the chat box

  function generateSessionId() {
    return Math.random().toString(36).substring(2, 15);
  }

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    setShowInitialMessage(false); // Hide the initial message after the first send
    setIsLoading(true); // Show the loading animation

    const newMessages = [...messages, { sender: 'user', type: 'text', text: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/search-books', {
          session_id: sessionId,
          query: input,
        },
        {
          timeout: 150000,
          headers: {
            'Content-Type': 'application/json', // Ensure proper headers
          },
        }
      );

      const reply = response.data;
      console.log(reply);

      // Check response type
      if (reply.profanity_found) {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            sender: 'bot',
            type: 'warning',
            text: reply.profanity_found,
          },
        ]);
      } else if (reply.no_matches_found) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', type: 'info', text: reply.no_matches_found },
        ]);
      } else if (reply.message) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', type: 'info', text: reply.message },
        ]);
      } else if (reply.issue_reason) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', type: 'info', text: 'Issue in OpenLibrary API: ' + reply.issue_reason },
        ]);
      } else if (reply.books) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', type: 'books', books: reply.books },
        ]);

        if (reply.further_chat) {
          setMessages((prevMessages) => [
            ...prevMessages,
            { sender: 'bot', type: 'text', text: reply.further_chat },
          ]);
        }
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', type: 'text', text: 'Unexpected response format.' + reply },
        ]);
      }
    } catch (error) {
      console.error('Error fetching data:', {
        message: error.message,
        stack: error.stack,
        name: error.name,
        ...(error.response && { response: error.response }),
      });

      // Optional: Extracting and displaying a more meaningful error message for the user
      const errorMessage =
        error.message || 'An unknown error occurred. Please try again later.';

      // Update messages state with detailed context for debugging (for developers) or user-friendly message
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          sender: 'bot',
          type: 'text',
          text: `An error occurred: ${errorMessage}`
        },
      ]);

      // Optionally add more debugging information for the developer
      if (process.env.NODE_ENV === 'development') {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            sender: 'bot',
            type: 'text',
            text: `Detailed error: ${JSON.stringify({
              name: error.name,
              message: error.message,
              stack: error.stack,
              ...(error.response && { response: error.response }),
            }, null, 2)}`,
          },
        ]);
      }
    } finally {
      setIsLoading(false); // Hide the loading animation
    }
  };

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]); // Scrolls to the bottom whenever messages change

  return (
    <div className="chat-container">
      <div className="chat-box" ref={chatBoxRef}>
        {showInitialMessage && (
          <div
            className="initial-message"
            style={{
              textAlign: 'center',
              fontSize: '20px',
              margin: '20px 0',
              color: '#aaa',
            }}>
            Please type your book search request:
          </div>
        )}
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.type === 'text' && <div>{msg.text}</div>}
            {msg.type === 'books' &&
              msg.books.map((book, idx) => (
                <div key={idx} className="book-entry">
                  <div className="book-title">{book.title}</div>
                  <div className="book-author">by {book.author_name}</div>
                  <div className="book-description">{book.brief_description}</div>
                  <div className="book-attribute">{book.number_of_pages_median} pages</div>
                  <div className="book-attribute">First published in {book.first_publish_year}</div>
                  <div style={{ display: "block" }}>
                    {book.ratings_average ? (
                    <>
                      <div className="book-attribute">Rating: {book.ratings_average}</div>
                      <div className="book-attribute">({book.ratings_count} given)</div>
                        {[5, 4, 3, 2, 1].map((rating) => (
                          <div key={rating} className="book-attribute">
                            {rating}&nbsp;
                            <img
                              src="star.png"
                              alt="Star"
                              style={{ width: "10px", height: "10px" }}
                            />: 
                            &nbsp;<b>{book[`ratings_count_${rating}`]}</b>
                          </div>
                        ))}
                    </>
                    ) : (
                      <div className="book-attribute">No ratings yet</div>
                    )}
                  </div>
                </div>
              ))}
              {msg.type === 'warning' && (
                <div className="warning-message">
                  <img
                    src="/warning-icon.png"
                    alt="Warning"
                    className="warning-icon"
                  />
                  <span>{msg.text}</span>
                </div>
              )}
              {msg.type === 'info' && (
                <div className="info-message">
                  <img
                    src="/info-icon.png"
                    alt="Info"
                    className="info-icon"
                  />
                  <span>{msg.text}</span>
                </div>
              )}
          </div>
        ))}
        {isLoading && (
          <div
            className="loading-animation"
            style={{
              textAlign: 'center',
              fontSize: '24px',
              margin: '10px 0',
              color: '#555',
            }}
          >
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        )}
      </div>
      <div className="input-box">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSend();
            }
          }}
          placeholder="Type your query..."
          style={{
            background:
              `linear-gradient(90deg, rgba(60,60,60,1) 0%, rgba(80,90,80,1) 25%, 
               rgba(100,100,100,1) 50%, rgba(80,90,80,1) 75%, rgba(60,60,60,1) 100%)`,
            color: 'white',
            border: 'none',
            padding: '10px',
            borderRadius: '4px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
            outline: 'none',
          }}
        />
        <button
        onClick={handleSend}
        style={{
          background:
            'linear-gradient(90deg, rgba(0,123,255,1) 0%, rgba(0,180,255,1) 50%, rgba(0,123,255,1) 100%)',
          color: 'white',
          border: 'none',
          padding: '10px 15px',
          borderRadius: '4px',
          cursor: 'pointer',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
        }}>
        Send
      </button>
      </div>
    </div>
  );
}

export default App;
