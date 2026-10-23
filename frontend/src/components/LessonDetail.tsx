import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '@/api/client'

interface Lesson {
  id: string
  title: string
  description: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimated_minutes: number
  sections: Section[]
}

interface Section {
  id: string
  title: string
  content: string
  examples: Example[]
  templates: Template[]
}

interface Example {
  title: string
  code: string
  language: string
}

interface Template {
  title: string
  content: string
  filename: string
}

export function LessonDetail() {
  const { id } = useParams<{ id: string }>()
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState<string | null>(null)

  useEffect(() => {
    async function fetchLesson() {
      try {
        setLoading(true)
        const data = await api.get<Lesson>(`/api/lessons/${id}`)
        setLesson(data)
      } catch (e) {
        setError('Failed to load lesson')
      } finally {
        setLoading(false)
      }
    }
    if (id) fetchLesson()
  }, [id])

  const copyToClipboard = async (text: string, label: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(label)
    setTimeout(() => setCopied(null), 2000)
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
        <div style={{ color: 'var(--color-text-muted)' }}>Loading lesson…</div>
      </div>
    )
  }

  if (error || !lesson) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <Link to="/" className="btn btn-primary">← Back to Lessons</Link>
      </div>
    )
  }

  return (
    <article>
      <Link to="/" className="btn btn-ghost" style={{ marginBottom: '1.5rem', display: 'inline-flex' }}>
        ← Back to Lessons
      </Link>

      <header style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
          <span className={`badge badge-${lesson.difficulty === 'beginner' ? 'success' : lesson.difficulty === 'intermediate' ? 'warning' : 'danger'}`}>
            {lesson.difficulty}
          </span>
          <span className="badge badge-primary">{lesson.category}</span>
          <span style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>⏱ {lesson.estimated_minutes} min</span>
        </div>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '0.75rem' }}>{lesson.title}</h1>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '1.125rem', maxWidth: '800px' }}>{lesson.description}</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: '2rem' }}>
        <div>
          {lesson.sections.map((section) => (
            <section key={section.id} className="card" style={{ marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1rem', paddingBottom: '0.75rem', borderBottom: '1px solid var(--color-border)' }}>
                {section.title}
              </h2>
              <div style={{ color: 'var(--color-text)', lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
                {section.content}
              </div>

              {section.examples.length > 0 && (
                <div style={{ marginTop: '1.5rem' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.75rem', color: 'var(--color-text-muted)' }}>Examples</h3>
                  {section.examples.map((ex, i) => (
                    <div key={i} style={{ marginBottom: '1rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--color-text-muted)' }}>{ex.title}</span>
                        <button
                          className="btn btn-ghost"
                          style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                          onClick={() => copyToClipboard(ex.code, `Example ${i + 1}`)}
                        >
                          {copied === `Example ${i + 1}` ? '✓ Copied' : 'Copy'}
                        </button>
                      </div>
                      <pre><code>{ex.code}</code></pre>
                    </div>
                  ))}
                </div>
              )}

              {section.templates.length > 0 && (
                <div style={{ marginTop: '1.5rem' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.75rem', color: 'var(--color-text-muted)' }}>Copy-Paste Templates</h3>
                  {section.templates.map((tmpl, i) => (
                    <div key={i} style={{ marginBottom: '1rem' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--color-text-muted)' }}>{tmpl.filename}</span>
                        <button
                          className="btn btn-primary"
                          style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                          onClick={() => copyToClipboard(tmpl.content, tmpl.filename)}
                        >
                          {copied === tmpl.filename ? '✓ Copied' : 'Copy Template'}
                        </button>
                      </div>
                      <pre><code>{tmpl.content}</code></pre>
                    </div>
                  ))}
                </div>
              )}
            </section>
          ))}
        </div>

        <aside style={{ position: 'sticky', top: '100px', height: 'fit-content' }}>
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem' }}>Contents</h3>
            <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {lesson.sections.map((section) => (
                <Link
                  key={section.id}
                  to={`#${section.id}`}
                  style={{
                    padding: '0.5rem 0.75rem',
                    borderRadius: 'var(--radius)',
                    fontSize: '0.875rem',
                    color: 'var(--color-text)',
                    background: 'transparent',
                    transition: 'background var(--transition)',
                  }}
                >
                  {section.title}
                </Link>
              ))}
            </nav>
          </div>
        </aside>
      </div>
    </article>
  )
}