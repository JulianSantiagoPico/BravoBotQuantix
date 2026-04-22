import { useEffect, useRef } from 'react'
import MessageBubble, { Message } from './MessageBubble'

interface ChatWindowProps {
  messages: Message[]
  isLoading: boolean
}

export default function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 space-y-5">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center text-gray-400 gap-3">
          <div className="w-16 h-16 rounded-full bg-pascual-blue flex items-center justify-center">
            <span className="text-white text-2xl font-bold">B</span>
          </div>
          <div>
            <p className="text-lg font-semibold text-pascual-blue">¡Hola! Soy BravoBot</p>
            <p className="text-sm mt-1">
              Pregúntame sobre programas, admisiones, costos o cualquier tema de la I.U. Pascual Bravo.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2 w-full max-w-md">
            {[
              '¿Qué programas de ingeniería ofrecen?',
              '¿Cuáles son los costos de matrícula?',
              '¿Cómo es el proceso de inscripción?',
              '¿Tienen becas disponibles?',
            ].map((suggestion) => (
              <div
                key={suggestion}
                className="bg-white border border-gray-200 rounded-lg px-3 py-2 text-xs text-gray-600 cursor-default shadow-sm"
              >
                {suggestion}
              </div>
            ))}
          </div>
        </div>
      )}

      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {isLoading && (
        <div className="flex gap-3 items-start">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-pascual-blue flex items-center justify-center text-white text-sm font-bold">
            B
          </div>
          <div className="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-100">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-pascual-blue rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <span className="w-2 h-2 bg-pascual-blue rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <span className="w-2 h-2 bg-pascual-blue rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
