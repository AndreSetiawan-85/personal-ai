"use client";

import { useEffect, useState } from "react";

type Message = {
  id: number;
  role: string;
  content: string;
};

export default function Home() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadHistory() {
    try {
      const response = await fetch(
        "http://localhost:8000/chat/history"
      );

      const data = await response.json();

      setMessages(data);

    } catch (error) {
      console.error(
        "Failed loading history",
        error
      );
    }
  }


  useEffect(() => {
    loadHistory();
  }, []);


  async function sendMessage() {
    if (!message.trim()) return;


    const userText = message;

    setMessage("");
    setLoading(true);


    const tempUserMessage: Message = {
      id: Date.now(),
      role: "user",
      content: userText,
    };


    setMessages((prev) => [
      ...prev,
      tempUserMessage,
    ]);


    try {
      const response = await fetch(
        "http://localhost:8000/chat/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: userText,
          }),
        }
      );


      if (!response.body) {
        throw new Error(
          "No response body"
        );
      }


      const reader =
        response.body.getReader();


      const decoder =
        new TextDecoder();


      let assistantText = "";


      const assistantId = Date.now() + 1;


      setMessages((prev) => [
        ...prev,
        {
          id: assistantId,
          role: "assistant",
          content: "",
        },
      ]);


      while (true) {

        const {
          done,
          value,
        } = await reader.read();


        if (done) break;


        const chunk =
          decoder.decode(value, {
            stream: true,
          });


        assistantText += chunk;


        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantId
              ? {
                  ...msg,
                  content: assistantText,
                }
              : msg
          )
        );
      }


    } catch (error) {

      console.error(error);


      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          content:
            "Error connecting to backend",
        },
      ]);

    }


    setLoading(false);
  }


  return (
    <main className="min-h-screen p-10">

      <h1 className="text-3xl font-bold mb-6">
        Personal AI Agent
      </h1>


      <div className="
        border
        rounded
        p-4
        min-h-96
        mb-6
        space-y-4
        whitespace-pre-wrap
      ">

        {messages.length === 0 && (
          <div>
            No conversation yet...
          </div>
        )}


        {messages.map((msg) => (

          <div
            key={msg.id}
            className={
              msg.role === "user"
                ? "text-right"
                : "text-left"
            }
          >

            <div
              className={
                msg.role === "user"
                  ? `
                    inline-block
                    bg-black
                    text-white
                    rounded
                    px-4
                    py-2
                  `
                  : `
                    inline-block
                    bg-gray-200
                    text-black
                    rounded
                    px-4
                    py-2
                  `
              }
            >
              {msg.content}
            </div>

          </div>

        ))}

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
        {loading
          ? "Thinking..."
          : "Send"}
      </button>


    </main>
  );
}