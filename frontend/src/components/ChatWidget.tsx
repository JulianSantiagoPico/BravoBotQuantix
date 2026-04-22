import { useState } from 'react'
import ChatWindow from './ChatWindow'
import InputBar from './InputBar'
import { Message } from './MessageBubble'
import axios from 'axios'

const API_URL = '/chat'

let msgCounter = 0
function nextId() {
  return `msg-${++msgCounter}`
}

/* ── Close icon ── */
function CloseIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
      <path d="M18 6 6 18M6 6l12 12" />
    </svg>
  )
}

/* ── Chat bubble icon (when closed) ── */
function ChatBubbleIcon() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  )
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
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
    <>
      {/* ═══════════════ CHAT PANEL ═══════════════ */}
      <div
        className={`chat-widget-panel ${isOpen ? 'chat-widget-open' : 'chat-widget-closed'}`}
        style={{
          position: 'fixed',
          bottom: '96px',
          right: '24px',
          width: '420px',
          height: '560px',
          zIndex: 9999,
          display: 'flex',
          flexDirection: 'column',
          borderRadius: '16px',
          overflow: 'hidden',
          boxShadow: isOpen ? '0 12px 48px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.05)' : 'none',
          opacity: isOpen ? 1 : 0,
          transform: isOpen ? 'translateY(0) scale(1)' : 'translateY(20px) scale(0.95)',
          pointerEvents: isOpen ? 'auto' : 'none',
          transition: 'opacity 0.3s ease, transform 0.3s ease',
          background: '#F2F6F9',
        }}
      >
        {/* Panel Header */}
        <div
          style={{
            background: 'linear-gradient(135deg, #001A34 0%, #0F385A 100%)',
            padding: '14px 18px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            flexShrink: 0,
          }}
        >
          <div
            style={{
              width: '38px',
              height: '38px',
              borderRadius: '50%',
              background: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              overflow: 'hidden',
              border: '2px solid rgba(2,153,216,0.3)',
              flexShrink: 0,
            }}
          >
            <img
              src="/Logo_1.png"
              alt="BravoBot"
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </div>
          <div style={{ flex: 1 }}>
            <div
              style={{
                color: '#fff',
                fontFamily: '"Roboto Condensed", sans-serif',
                fontWeight: 700,
                fontSize: '16px',
                lineHeight: 1.2,
              }}
            >
              BravoBot
            </div>
            <div
              style={{
                color: 'rgba(255,255,255,0.65)',
                fontSize: '11px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
              }}
            >
              <span
                style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  background: '#00B87C',
                  display: 'inline-block',
                }}
              />
              Asistente institucional
            </div>
          </div>

          {/* New conversation button */}
          {messages.length > 0 && (
            <button
              onClick={() => setMessages([])}
              style={{
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '8px',
                color: 'rgba(255,255,255,0.7)',
                fontSize: '11px',
                padding: '4px 10px',
                cursor: 'pointer',
                fontFamily: '"Open Sans", sans-serif',
                transition: 'all 0.2s',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.18)'
                e.currentTarget.style.color = '#fff'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(255,255,255,0.1)'
                e.currentTarget.style.color = 'rgba(255,255,255,0.7)'
              }}
              title="Nueva conversación"
            >
              Nueva
            </button>
          )}

          {/* Close button */}
          <button
            onClick={() => setIsOpen(false)}
            style={{
              background: 'rgba(255,255,255,0.1)',
              border: 'none',
              borderRadius: '8px',
              color: '#fff',
              cursor: 'pointer',
              padding: '6px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background 0.2s',
            }}
            onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(255,255,255,0.2)')}
            onMouseLeave={(e) => (e.currentTarget.style.background = 'rgba(255,255,255,0.1)')}
            aria-label="Cerrar chat"
          >
            <CloseIcon />
          </button>
        </div>

        {/* Chat body */}
        <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <ChatWindow messages={messages} isLoading={isLoading} onSuggestion={handleSuggestion} />
          <InputBar onSend={sendMessage} disabled={isLoading} />
        </div>
      </div>

      {/* ═══════════════ FLOATING BUTTON ═══════════════ */}
      <button
        id="chat-widget-toggle"
        onClick={() => setIsOpen(!isOpen)}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          border: 'none',
          cursor: 'pointer',
          zIndex: 10000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.3s ease',
          background: isOpen
            ? 'linear-gradient(135deg, #001A34 0%, #0F385A 100%)'
            : 'linear-gradient(135deg, #0299D8 0%, #027ab5 100%)',
          color: '#fff',
          boxShadow: isOpen
            ? '0 4px 16px rgba(0,26,52,0.4)'
            : '0 4px 20px rgba(2,153,216,0.45)',
          overflow: 'hidden',
          animation: isOpen ? 'none' : 'chatWidgetPulse 3s ease-in-out infinite',
        }}
        aria-label={isOpen ? 'Cerrar chat' : 'Abrir chat con BravoBot'}
      >
        {isOpen ? (
          <CloseIcon />
        ) : (
          <img
            src="/Logo_1.png"
            alt="BravoBot"
            style={{ width: '42px', height: '42px', objectFit: 'cover', borderRadius: '50%' }}
          />
        )}
      </button>

      {/* Tooltip (only when closed) */}
      {!isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '90px',
            right: '24px',
            background: '#001A34',
            color: '#fff',
            fontSize: '12px',
            fontFamily: '"Open Sans", sans-serif',
            fontWeight: 600,
            padding: '6px 14px',
            borderRadius: '8px',
            zIndex: 10000,
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            whiteSpace: 'nowrap',
            animation: 'chatTooltipFade 0.5s ease 2s both',
            pointerEvents: 'none',
          }}
        >
          Chatea con BravoBot 💬
          <div
            style={{
              position: 'absolute',
              bottom: '-5px',
              right: '20px',
              width: '10px',
              height: '10px',
              background: '#001A34',
              transform: 'rotate(45deg)',
            }}
          />
        </div>
      )}

      {/* Animations */}
      <style>{`
        @keyframes chatWidgetPulse {
          0%, 100% { box-shadow: 0 4px 20px rgba(2,153,216,0.45); }
          50% { box-shadow: 0 4px 30px rgba(2,153,216,0.65), 0 0 0 8px rgba(2,153,216,0.1); }
        }
        @keyframes chatTooltipFade {
          from { opacity: 0; transform: translateY(4px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @media (max-width: 480px) {
          .chat-widget-panel {
            width: calc(100vw - 16px) !important;
            height: calc(100vh - 120px) !important;
            right: 8px !important;
            bottom: 80px !important;
            border-radius: 12px !important;
          }
        }
      `}</style>
    </>
  )
}
