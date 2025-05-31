// Frontend: React Chat App using the Groq-based LangChain API
// Assumes you have an Express backend running the given LangChain code exposed at /api/chat

import React, { useState } from "react";
import axios from "axios";

const ChatApp = () => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    const userMessage = { sender: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    try {
      const response = await axios.post(process.env.REACT_APP_API+"/api/chat", { query });
      const botMessage = {
        sender: "bot",
        text: response.data.result,
        sources: response.data.sources,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Error occurred." }]);
    }
    setQuery("");
    setLoading(false);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Groq Chat Assistant</h1>
      <div className="border rounded p-4 h-96 overflow-y-auto bg-white mb-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-2 ${msg.sender === "user" ? "text-right" : "text-left"}`}
          >
            <p className={`inline-block px-3 py-2 rounded-md ${msg.sender === "user" ? "bg-blue-200" : "bg-gray-100"}`}>
              {msg.text}
            </p>
            {msg.sources && (
              <ul className="text-[10px] text-gray-500 mt-1">
                {msg.sources.map((src, j) => (
                  <li key={j}>Source: {src}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          className="flex-1 border rounded px-3 py-2"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask a question..."
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Loading..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default ChatApp;
