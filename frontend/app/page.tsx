"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");

  async function sendMessage() {
    const response = await fetch(
      "http://localhost:8000/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      }
    );

    const data = await response.json();

    setReply(data.reply);
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center">

      <h1 className="text-4xl font-bold">
        Personal AI
      </h1>

      <p className="mt-4 text-gray-600">
        Your personal AI assistant
      </p>

      <div className="mt-8 w-96">

        <input
          className="border rounded p-3 w-full"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message..."
        />

        <button
          onClick={sendMessage}
          className="mt-3 bg-black text-white px-4 py-2 rounded"
        >
          Send
        </button>

        <div className="mt-5 border rounded p-3">
          {reply}
        </div>

      </div>

    </main>
  );
}