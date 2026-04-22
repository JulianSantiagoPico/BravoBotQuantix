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

  const handleSend = async (text: string) => {
    const userMsg: Message = {
      id: nextId(),
      role: 'user',
      content: text,
    }
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

  return (
    <div className="flex flex-col h-screen bg-pascual-gray">
      {/* Header */}
      <header className="bg-pascual-blue text-white px-4 py-3 shadow-md flex-shrink-0">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-pascual-orange flex items-center justify-center font-bold text-lg flex-shrink-0">
            B
          </div>
          <div>
            <h1 className="font-bold text-base leading-tight">BravoBot</h1>
            <p className="text-xs text-blue-200 leading-tight">
              Asistente Institucional — I.U. Pascual Bravo
            </p>
          </div>
          <div className="ml-auto flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-xs text-blue-200">En línea</span>
          </div>
        </div>
      </header>

      {/* Chat area */}
      <main className="flex-1 overflow-hidden flex flex-col max-w-4xl w-full mx-auto">
        <ChatWindow messages={messages} isLoading={isLoading} />
        <InputBar onSend={handleSend} disabled={isLoading} />
      </main>
    </div>
  )
}
