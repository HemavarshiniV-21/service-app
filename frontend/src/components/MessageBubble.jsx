import { memo } from 'react'

function formatTime(timestamp) {
  const date = new Date(timestamp)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function MessageBubble({ message }) {
  const { role, text, timestamp, status } = message
  const isUser = role === 'user'

  return (
    <div className={`message ${isUser ? 'user' : 'bot'} ${status || ''}`}>
      <div className="bubble">
        <p className="message-text">{text}</p>
        <div className="message-meta">
          <span className="message-time">{formatTime(timestamp)}</span>
          {status === 'loading' ? <span className="message-status">Typing…</span> : null}
        </div>
      </div>
    </div>
  )
}

export default memo(MessageBubble)
