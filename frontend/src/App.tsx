import { useState } from 'react'
import axios from 'axios'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import { Message } from './components/MessageBubble'

const API_URL = '/chat'

let msgCounter = 0
function nextId() {
  return `msg-${++msgCounter}`
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (text: string) => {
    const userMsg: Message = { id: nextId(), role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    try {
      const { data } = await axios.post(API_URL, { query: text })
      const botMsg: Message = {
        id: nextId(),
        role: 'bot',
        content: data.respuesta,
        fuentes: data.fuentes,
        categoria: data.categoria,
      }
      setMessages((prev) => [...prev, botMsg])
    } catch {
      const errorMsg: Message = {
        id: nextId(),
        role: 'bot',
        content:
          'Ocurrió un error al procesar tu pregunta. Por favor intenta de nuevo o visita pascualbravo.edu.co directamente.',
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSuggestion = (text: string) => {
    if (isLoading) return
    sendMessage(text)
  }

  return (
    <div className="flex flex-col h-full bg-pb-gray-light">

      {/* ══════════════════════════ CHAT AREA ══════════════════════════ */}
      <main className="relative flex-1 overflow-hidden flex flex-col max-w-[1250px] w-full mx-auto">

        {/* Floating "Nueva conversación" button */}
        {messages.length > 0 && (
          <button
            id="clear-chat-btn"
            onClick={() => setMessages([])}
            className="absolute top-3 right-4 z-10 flex items-center gap-1.5 text-xs font-body text-pb-gray
                       bg-white/90 backdrop-blur-sm border border-gray-200 rounded-lg px-3 py-1.5
                       hover:text-pb-red hover:border-pb-red/30 transition-all duration-200 shadow-sm"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Nueva conversación
          </button>
        )}

        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          onSuggestion={handleSuggestion}
        />
        <InputBar onSend={sendMessage} disabled={isLoading} />
      </main>
    </div>
  )
}
