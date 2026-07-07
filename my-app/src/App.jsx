import { FaUser } from "react-icons/fa";
import { BsRobot } from "react-icons/bs";

import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const chatBoxRef = useRef(null);
  const [relatedQuestions, setRelatedQuestions] = useState([
    "What is a linked list?",
    "Explain binary search",
    "Time complexity basics",
    "What is recursion?"
  ]);
  const [typedText, setTypedText] = useState("");
  const scrollToBottom = () => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat, isLoading]);

  useEffect(() => {
    const text = "Ask questions about Data Structures and Algorithms";
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        setTypedText(text.slice(0, index + 1));
        index++;
      } else {
        clearInterval(interval);
      }
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!message.trim() || isLoading) return;

    const now = new Date();
    const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const userMessage = {
      role: "user",
      text: message,
      timestamp: timestamp,
    };

    setChat((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setMessage("");

    try {
      const response = await axios.post("http://localhost:8000/chat", {
        query: message,
      });

      const botTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      setChat((prev) => [
        ...prev,
        {
          role: "bot",
          text: response.data.answer,
          sources: response.data.sources || [],
          timestamp: botTimestamp,
        },
      ]);

      
      // Update related questions based on user query
      const newRelatedQuestions = generateRelatedQuestions(message);
      setRelatedQuestions(newRelatedQuestions);
    } catch (error) {
      const errorTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      setChat((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Backend not reachable",
          timestamp: errorTimestamp,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const generateRelatedQuestions = (query) => {
    const queryLower = query.toLowerCase();
    const dsaQuestions = {
      "linked list": [
        "What are the types of linked lists?",
        "How to reverse a linked list?",
        "Linked list vs Array comparison",
        "Detect cycle in linked list"
      ],
      "binary search": [
        "Time complexity of binary search",
        "Binary search implementation",
        "Binary search tree vs binary search",
        "When to use binary search?"
      ],
      "sorting": [
        "Bubble sort algorithm",
        "Quick sort vs Merge sort",
        "Time complexity of sorting algorithms",
        "Stable vs unstable sorting"
      ],
      "recursion": [
        "Recursion vs iteration",
        "Base case in recursion",
        "Stack overflow in recursion",
        "Recursive vs iterative approach"
      ],
      "array": [
        "Dynamic array vs static array",
        "2D array operations",
        "Array time complexity",
        "Array vs linked list"
      ],
      "tree": [
        "Binary tree traversal",
        "AVL tree rotation",
        "Tree vs Graph",
        "Height vs depth of tree"
      ],
      "graph": [
        "BFS vs DFS traversal",
        "Dijkstra's algorithm",
        "Graph representation methods",
        "Topological sorting"
      ],
      "stack": [
        "Stack implementation using array",
        "Queue vs Stack",
        "Stack applications",
        "Stack overflow explanation"
      ],
      "queue": [
        "Circular queue implementation",
        "Priority queue",
        "Queue vs Stack",
        "Deque operations"
      ],
      "hash": [
        "Hash collision resolution",
        "Hash table implementation",
        "Load factor in hashing",
        "Hash map vs hash table"
      ]
    };

    for (const [keyword, questions] of Object.entries(dsaQuestions)) {
      if (queryLower.includes(keyword)) {
        return questions;
      }
    }

    // Default related questions if no match
    return [
      "What is time complexity?",
      "Explain space complexity",
      "Big O notation examples",
      "Data structures basics"
    ];
  };

  return (
    <>
    <>
  <div className="background-title">
    <div className="floating-shapes">
      <div className="shape shape-1"></div>
      <div className="shape shape-2"></div>
      <div className="shape shape-3"></div>
      <div className="shape shape-4"></div>
      <div className="shape shape-5"></div>
    </div>
    <h1 className="title-animate">DSA Chat Bot</h1>
    <p className="typing-text">{typedText}<span className="cursor">|</span></p>
   
  </div>
</>

      {!isOpen && (
        <button
          className="chat-icon"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
        >
          💬
        </button>
      )}

      {isOpen && (
        <div className="chat-widget">
          <div className="chat-header">
            <div className="chat-header-info">
              <span className="chat-header-title">DSA Chat Bot</span>
              <span className="chat-header-status">Online</span>
            </div>
            <button
              className="chat-header-close"
              onClick={() => setIsOpen(false)}
            >
              ✕
            </button>
          </div>

          <div className="chat-box" ref={chatBoxRef}>
            {chat.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                {msg.role === "bot" && (
                  <div className="message-avatar">
                    <BsRobot />
                  </div>
                )}
                <div className="message-content">
                  <div className="message-bubble">
                    {msg.text}
                  </div>
                  <div className="message-meta">
                    <span className="timestamp">{msg.timestamp}</span>
                    {msg.role === "user" && <span className="read-receipt">✓✓</span>}
                  </div>
                  {msg.role === "bot" &&
                    msg.sources &&
                    msg.sources.length > 0 && (
                      <div className="sources">
                        <small>Sources</small>
                        {msg.sources.map((src, i) => (
                          <div key={i} className="source-item">
                            📄 {src.document} (Page {src.page})
                          </div>
                        ))}
                      </div>
                    )}
                </div>
                {msg.role === "user" && (
                  <div className="message-avatar">
                    <FaUser />
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="message bot">
                <div className="message-avatar">
                  <BsRobot />
                </div>
                <div className="message-content">
                  <div className="loading">
                    <div className="loading-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span>Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="chat-suggestions">
            {relatedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => {
                  setMessage(question);
                }}
              >
                {question}
              </button>
            ))}
          </div>

          <div className="input-area">
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here..."
              disabled={isLoading}
            />
            <button onClick={sendMessage} disabled={isLoading || !message.trim()}>
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default App;