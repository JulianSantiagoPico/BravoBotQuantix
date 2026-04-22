import SourcesList from './SourcesList'

export interface Message {
  id: string
  role: 'user' | 'bot'
  content: string
  fuentes?: string[]
  categoria?: string
}

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} items-start`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ${
          isUser ? 'bg-pascual-orange' : 'bg-pascual-blue'
        }`}
      >
        {isUser ? 'Tú' : 'B'}
      </div>

      {/* Bubble */}
      <div className={`max-w-[75%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
            isUser
              ? 'bg-pascual-blue text-white rounded-tr-sm'
              : 'bg-white text-gray-800 rounded-tl-sm shadow-sm border border-gray-100'
          }`}
        >
          {message.content}
        </div>

        {!isUser && message.fuentes && message.fuentes.length > 0 && (
          <div className="mt-1 px-1">
            <SourcesList fuentes={message.fuentes} />
          </div>
        )}
      </div>
    </div>
  )
}
