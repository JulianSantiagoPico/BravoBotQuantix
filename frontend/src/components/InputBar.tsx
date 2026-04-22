import { useState, KeyboardEvent } from 'react'

interface InputBarProps {
  onSend: (text: string) => void
  disabled: boolean
}

export default function InputBar({ onSend, disabled }: InputBarProps) {
  const [value, setValue] = useState('')

  const handleSend = () => {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue('')
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="border-t border-gray-200 bg-white px-4 py-3">
      <div className="flex items-end gap-2 max-w-4xl mx-auto">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
          placeholder="Escribe tu pregunta aquí..."
          className="flex-1 resize-none rounded-xl border border-gray-300 px-4 py-3 text-sm
                     focus:outline-none focus:ring-2 focus:ring-pascual-blue focus:border-transparent
                     disabled:bg-gray-50 disabled:text-gray-400 max-h-32 overflow-y-auto
                     transition-all"
          style={{ minHeight: '44px' }}
          onInput={(e) => {
            const target = e.target as HTMLTextAreaElement
            target.style.height = 'auto'
            target.style.height = `${Math.min(target.scrollHeight, 128)}px`
          }}
        />
        <button
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          className="flex-shrink-0 w-11 h-11 rounded-xl bg-pascual-blue text-white
                     flex items-center justify-center transition-all
                     hover:bg-pascual-lightBlue disabled:opacity-40 disabled:cursor-not-allowed
                     active:scale-95"
          aria-label="Enviar mensaje"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
      <p className="text-center text-xs text-gray-400 mt-2">
        BravoBot responde únicamente con información oficial del sitio de la I.U. Pascual Bravo.
      </p>
    </div>
  )
}
