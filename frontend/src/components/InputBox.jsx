import { useEffect, useRef } from 'react'

function InputBox({ value, onChange, onSend, disabled }) {
  const inputRef = useRef(null)

  useEffect(() => {
    if (!inputRef.current) return
    inputRef.current.focus()
  }, [])

  const send = () => {
    const trimmed = value.trim()
    if (!trimmed) return
    onSend(trimmed)
  }

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      send()
    }
  }

  return (
    <form
      className="input-box"
      onSubmit={(event) => {
        event.preventDefault()
        send()
      }}
    >
      <textarea
        ref={inputRef}
        className="input-text"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
        placeholder="Ask about buying, repairs, maintenance, costs..."
        disabled={disabled}
        aria-label="Type your question"
      />

      <button className="btn btn-send" type="submit" disabled={disabled || !value.trim()}>
        Send
      </button>
    </form>
  )
}

export default InputBox
