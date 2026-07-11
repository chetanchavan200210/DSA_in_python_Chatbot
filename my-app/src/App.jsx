import { FaUser, FaUpload, FaPaperclip, FaTrash, FaCopy, FaCheck } from "react-icons/fa";
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
    "What are the types of dental radiographs?",
    "Explain linked lists in Python",
    "What is bitewing radiography?",
    "How to implement binary search in Python?"
  ]);
  const [typedText, setTypedText] = useState("");
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('chatSessionId') || generateSessionId();
  });
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [copiedMessage, setCopiedMessage] = useState(null);
  const fileInputRef = useRef(null);

  function generateSessionId() {
    const id = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('chatSessionId', id);
    return id;
  }
  const scrollToBottom = () => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chat, isLoading]);

  useEffect(() => {
    const text = "Dental Radiology Atlas & DSA in Python";
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
        session_id: sessionId,
      });

      const botTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      setChat((prev) => [
        ...prev,
        {
          role: "bot",
          text: response.data.answer,
          sources: response.data.sources || [],
          related_questions: response.data.related_questions || [],
          timestamp: botTimestamp,
        },
      ]);

      // Update related questions from response or generate based on query
      if (response.data.related_questions && response.data.related_questions.length > 0) {
        setRelatedQuestions(response.data.related_questions);
      } else {
        const newRelatedQuestions = generateRelatedQuestions(message);
        setRelatedQuestions(newRelatedQuestions);
      }
    } catch (error) {
      const errorTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      setChat((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Backend not reachable. Please ensure the server is running.",
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

  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadedFiles((prev) => [...prev, {
        name: response.data.filename,
        type: response.data.file_type,
        message: response.data.message,
        uploadedAt: new Date().toLocaleTimeString(),
      }]);

      // Add system message about successful upload
      const uploadTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setChat((prev) => [
        ...prev,
        {
          role: "bot",
          text: `✅ File "${response.data.filename}" uploaded successfully. ${response.data.message}`,
          timestamp: uploadTimestamp,
        },
      ]);

      setShowUploadModal(false);
    } catch (error) {
      const errorTimestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setChat((prev) => [
        ...prev,
        {
          role: "bot",
          text: `❌ Upload failed: ${error.response?.data?.detail || error.message}`,
          timestamp: errorTimestamp,
        },
      ]);
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const clearChat = () => {
    setChat([]);
    setRelatedQuestions([
      "What are the types of dental radiographs?",
      "Explain linked lists in Python",
      "What is bitewing radiography?",
      "How to implement binary search in Python?"
    ]);
    const newSessionId = generateSessionId();
    setSessionId(newSessionId);
  };

  const copyToClipboard = (text, messageId) => {
    navigator.clipboard.writeText(text);
    setCopiedMessage(messageId);
    setTimeout(() => setCopiedMessage(null), 2000);
  };

  const generateRelatedQuestions = (query) => {
    const queryLower = query.toLowerCase();
    const dentalQuestions = {
      "radiograph": [
        "Types of dental radiographs",
        "Periapical vs bitewing radiographs",
        "Panoramic radiography basics",
        "Cone beam CT applications"
      ],
      "caries": [
        "Detecting dental caries on X-rays",
        "Classification of caries",
        "Interproximal caries detection",
        "Root caries diagnosis"
      ],
      "periapical": [
        "Periapical radiograph techniques",
        "Interpreting periapical lesions",
        "Periapical vs panoramic",
        "PA radiograph positioning"
      ],
      "periodontal": [
        "Periodontal disease on radiographs",
      "Bone loss patterns",
        "Furcation involvement detection",
        "Periodontal radiograph analysis"
      ],
      "impaction": [
        "Third molar impaction classification",
        "Impacted tooth radiograph signs",
        "Surgical planning for impactions",
        "Complications of impactions"
      ],
      "cyst": [
        "Radicular cyst characteristics",
        "Dentigerous cyst radiograph features",
        "Odontogenic vs non-odontogenic cysts",
        "Cyst vs tumor differentiation"
      ],
      "trauma": [
        "Dental trauma radiograph assessment",
        "Fracture patterns on X-rays",
        "Avulsion injury evaluation",
        "Root fracture detection"
      ],
      "endodontic": [
        "Endodontic treatment radiograph evaluation",
        "Root canal filling assessment",
        "Post-treatment radiograph analysis",
        "Failed endodontic therapy signs"
      ],
      "bone": [
        "Normal bone patterns on radiographs",
        "Osteoporosis dental radiograph signs",
        "Bone quality assessment",
        "Radiographic bone density"
      ],
      "interpretation": [
        "Radiograph interpretation basics",
        "Common radiographic errors",
        "Artifact identification",
        "Normal anatomy vs pathology"
      ]
    };

    const dsaQuestions = {
      "linked list": [
        "What are the types of linked lists in Python?",
        "How to reverse a linked list in Python?",
        "Linked list vs Array in Python",
        "Detect cycle in linked list Python"
      ],
      "binary search": [
        "Time complexity of binary search",
        "Binary search implementation in Python",
        "Binary search tree vs binary search",
        "When to use binary search in Python?"
      ],
      "sorting": [
        "Bubble sort algorithm in Python",
        "Quick sort vs Merge sort in Python",
        "Time complexity of sorting algorithms",
        "Stable vs unstable sorting"
      ],
      "recursion": [
        "Recursion vs iteration in Python",
        "Base case in recursion",
        "Stack overflow in recursion",
        "Recursive vs iterative approach"
      ],
      "array": [
        "Python list vs array",
        "2D array operations in Python",
        "Array time complexity",
        "Array vs linked list"
      ],
      "tree": [
        "Binary tree traversal in Python",
        "AVL tree rotation",
        "Tree vs Graph",
        "Height vs depth of tree"
      ],
      "graph": [
        "BFS vs DFS traversal in Python",
        "Dijkstra's algorithm in Python",
        "Graph representation methods",
        "Topological sorting"
      ],
      "stack": [
        "Stack implementation using Python list",
        "Queue vs Stack",
        "Stack applications",
        "Stack overflow explanation"
      ],
      "queue": [
        "Queue implementation in Python",
        "Priority queue in Python",
        "Queue vs Stack",
        "Deque operations"
      ],
      "hash": [
        "Hash collision resolution",
        "Python dictionary implementation",
        "Load factor in hashing",
        "Hash map vs hash table"
      ],
      "python": [
        "Python list operations",
        "Python dictionary methods",
        "Python set operations",
        "Python tuple vs list"
      ],
      "algorithm": [
        "Algorithm complexity analysis",
        "Big O notation in Python",
        "Space complexity basics",
        "Algorithm design patterns"
      ]
    };

    // Check dental questions first
    for (const [keyword, questions] of Object.entries(dentalQuestions)) {
      if (queryLower.includes(keyword)) {
        return questions;
      }
    }

    // Check DSA questions
    for (const [keyword, questions] of Object.entries(dsaQuestions)) {
      if (queryLower.includes(keyword)) {
        return questions;
      }
    }

    // Default related questions if no match - mix of both topics
    return [
      "What are the types of dental radiographs?",
      "How to implement linked list in Python?",
      "Binary search in Python",
      "Radiographic anatomy basics"
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
    <h1 className="title-animate">Dental Radiology & Python DSA</h1>
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
              <span className="chat-header-title">Radiology & Python DSA Assistant</span>
              <span className="chat-header-status">Online</span>
            </div>
            <div className="chat-header-actions">
              <button
                className="chat-header-action"
                onClick={() => setShowUploadModal(true)}
                title="Upload file"
              >
                <FaUpload />
              </button>
              <button
                className="chat-header-action"
                onClick={clearChat}
                title="Clear chat"
              >
                <FaTrash />
              </button>
              <button
                className="chat-header-close"
                onClick={() => setIsOpen(false)}
              >
                ✕
              </button>
            </div>
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
                  <button
                    className="copy-button"
                    onClick={() => copyToClipboard(msg.text, index)}
                    title="Copy message"
                  >
                    {copiedMessage === index ? <FaCheck /> : <FaCopy />}
                  </button>
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
            <button
              className="attach-button"
              onClick={() => fileInputRef.current.click()}
              title="Attach file"
            >
              <FaPaperclip />
            </button>
            <input
              type="file"
              ref={fileInputRef}
              style={{ display: 'none' }}
              onChange={handleFileSelect}
            />
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

      {showUploadModal && (
        <div className="upload-modal" onClick={() => setShowUploadModal(false)}>
          <div className="upload-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="upload-modal-header">
              <h3>Upload Document</h3>
              <button onClick={() => setShowUploadModal(false)}>✕</button>
            </div>
            <div
              className="upload-dropzone"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => fileInputRef.current.click()}
            >
              <FaUpload className="upload-icon" />
              <p>Drag & drop a file here, or click to select</p>
              <p className="upload-hint">Supports PDF, images, and text files</p>
            </div>
            {uploadedFiles.length > 0 && (
              <div className="uploaded-files-list">
                <h4>Uploaded Files</h4>
                {uploadedFiles.map((file, index) => (
                  <div key={index} className="uploaded-file-item">
                    <span className="file-name">📄 {file.name}</span>
                    <span className="file-type">({file.type})</span>
                    <span className="file-time">{file.uploadedAt}</span>
                  </div>
                ))}
              </div>
            )}
            {isUploading && (
              <div className="upload-progress">
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span>Uploading and processing...</span>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

export default App;