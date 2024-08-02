import React, { useState, useEffect } from "react";
import Chat from "./Chat";
import { SlArrowUpCircle } from "react-icons/sl";
import { FaRegStopCircle } from "react-icons/fa";
import api from "../api";

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState("");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    getNotes();
  }, []);

  const getNotes = () => {
    api
      .get("/api/message/")
      .then((res) => res.data)
      .then((data) => {
        setMessages(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const handleChat = (e) => {
    e.preventDefault();
    setLoading(true);
    api
      .post("/api/message/", { message: text })
      .then((res) => {
        if (res.status === 201) console.log("Message received successfully!");
        else alert("Failed to send message.");
        getNotes();
      })
      .catch((err) => alert(err));
    setLoading(false);
    setText("");
  };

  return (
    <div className="bg-blue-400 text-blue-500 text-3xl min-h-screen flex flex-col justify-center items-center">
      <div
        className={`w-[90%] sm:w-[60%] bg-gray-600 h-[450px] border-none rounded-2xl shadow-2xl overflow-hidden flex flex-col ${
          messages.length === 0 ? "justify-center items-center" : ""
        }`}
      >
        <div className="flex-grow overflow-auto">
          {messages.length !== 0 ? (
            messages.map((message) => (
              <div className="py-3 px-4" key={message.id}>
                <Chat message={message} />
              </div>
            ))
          ) : (
            <h1 className="text-white text-4xl text-center">
              Ask me a <span className="text-blue-500">question</span>!
            </h1>
          )}
        </div>

        <div className="p-4 relative w-full">
          <input
            value={text}
            type="text"
            placeholder="Message Ai"
            onChange={(e) => setText(e.target.value)}
            className="input input-bordered text-white w-full pr-11"
          />
          <button
            onClick={handleChat}
            className="absolute right-7 top-2/4 transform -translate-y-2/4"
          >
            {!loading ? (
              <SlArrowUpCircle className="w-6 h-6 text-gray-500 hover:text-white" />
            ) : (
              <FaRegStopCircle className="w-6 h-6 text-gray-500 hover:text-white" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
