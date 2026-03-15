import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'

function ChatBox({ messages }) {
  const scrollRef = useRef(null)

  useEffect(() => {
    if (!scrollRef.current) return
    scrollRef.current.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="chat-box" role="log" aria-live="polite">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
      <div ref={scrollRef} />
    </div>
  )
}

export default ChatBox
