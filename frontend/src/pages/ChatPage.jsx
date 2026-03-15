import { useCallback, useMemo, useState } from 'react'
import ChatBox from '../components/ChatBox'
import InputBox from '../components/InputBox'
import '../App.css'

const CHAT_API_URL = 'http://127.0.0.1:8000/chat'

function createMessage(text, role = 'user', status = 'sent') {
  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    role,
    text,
    timestamp: Date.now(),
    status,
  }
}

function ChatPage() {
  const [messages, setMessages] = useState([
    createMessage(
      'Hi there! Ask me anything about buying, selling, repairs, or maintenance for your vehicle.',
      'bot',
    ),
  ])
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim() || loading) return
      setError(null)

      const userMessage = createMessage(text, 'user')
      setMessages((prev) => [...prev, userMessage])
      setDraft('')
      setLoading(true)

      try {
        const response = await fetch(CHAT_API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: text }),
        })

        if (!response.ok) {
          throw new Error(`Server returned ${response.status}`)
        }

        const payload = await response.json()
        const reply = payload?.chatbot_reply ?? 'Sorry, I did not receive a response.'

        const botMessage = createMessage(reply, 'bot')
        setMessages((prev) => [...prev, botMessage])
      } catch (err) {
        console.error(err)
        setError('Unable to reach the service. Please try again.')
        const errMessage = createMessage(
          'There was an error reaching the service. Please check your connection or try again.',
          'bot',
        )
        setMessages((prev) => [...prev, errMessage])
      } finally {
        setLoading(false)
      }
    },
    [loading],
  )

  const clearChat = () => {
    setError(null)
    setMessages([
      createMessage(
        'Hi there! Ask me anything about buying, selling, repairs, or maintenance for your vehicle.',
        'bot',
      ),
    ])
    setDraft('')
  }

  const showTyping = useMemo(() => loading && messages.length > 0, [loading, messages.length])

  return (
    <div className="chat-page">
      <header className="chat-header">
        <div>
          <h1>Service Center Chatbot</h1>
          <p className="subtitle">Ask questions about buying, selling, repairs, and maintenance.</p>
        </div>

        <div className="header-controls">
          <button className="btn btn-clear" type="button" onClick={clearChat} disabled={loading}>
            Clear
          </button>
        </div>
      </header>

      <div className="chat-container">
        <ChatBox messages={messages} />
        {showTyping && (
          <div className="typing-indicator" aria-live="polite">
            <span className="dot" />
            <span className="dot" />
            <span className="dot" />
          </div>
        )}

        {error && <div className="error-banner">{error}</div>}

        <div className="chat-input">
          <InputBox value={draft} onChange={setDraft} onSend={sendMessage} disabled={loading} />
        </div>
      </div>
    </div>
  )
}

export default ChatPage
