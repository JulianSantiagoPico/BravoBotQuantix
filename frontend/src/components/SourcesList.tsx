import { useState } from 'react'

interface SourcesListProps {
  fuentes: string[]
}

export default function SourcesList({ fuentes }: SourcesListProps) {
  const [open, setOpen] = useState(false)

  if (!fuentes || fuentes.length === 0) return null

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 text-xs text-pascual-blue hover:text-pascual-orange transition-colors"
      >
        <svg
          className={`w-3 h-3 transition-transform ${open ? 'rotate-90' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
        {open ? 'Ocultar fuentes' : `Ver fuentes (${fuentes.length})`}
      </button>

      {open && (
        <ul className="mt-1 space-y-1 pl-4">
          {fuentes.map((url, i) => (
            <li key={i}>
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:text-pascual-orange underline break-all transition-colors"
              >
                {url}
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
