"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    if (!message.trim()) return;

    setReply("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/chat/stream",
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

      if (!response.body) {
        throw new Error("No response body");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, {
          stream: true,
        });

        console.log("CHUNK:", chunk);

        setReply((prev) => prev + chunk);
      }

    } catch (error) {
      console.error(error);
      setReply("Error connecting to backend");
    }

    setLoading(false);
  }

  return (
    <main className="min-h-screen p-10">

      <h1 className="text-3xl font-bold mb-6">
        Personal AI Agent
      </h1>


      <div
        className="
          mb-6
          border
          rounded
          p-4
          min-h-40
          whitespace-pre-wrap
        "
      >
        {
          reply ||
          "AI response will appear here..."
        }
      </div>


      <textarea
        className="
          border
          rounded
          w-full
          p-3
        "
        rows={4}
        value={message}
        onChange={(e) =>
          setMessage(e.target.value)
        }
        placeholder="Ask something..."
      />


      <button
        className="
          mt-4
          bg-black
          text-white
          px-5
          py-2
          rounded
          disabled:opacity-50
        "
        onClick={sendMessage}
        disabled={loading}
      >
        {
          loading
          ? "Thinking..."
          : "Send"
        }
      </button>

    </main>
  );
}