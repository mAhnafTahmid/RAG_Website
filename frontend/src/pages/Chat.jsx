import React from "react";

const Chat = ({ message }) => {
  return (
    <div>
      <div className="chat chat-end">
        <div className="chat-bubble">{message.message}</div>
      </div>
      <div className="chat chat-start">
        <div className="chat-bubble">{message.ai}</div>
      </div>
    </div>
  );
};

export default Chat;
