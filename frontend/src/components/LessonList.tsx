import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/api/client'

interface Lesson {
  id: string
  title: string
  description: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  estimated_minutes: number
}

export function LessonList() {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')

  useEffect(() => {
    async function fetchLessons() {
      try {
        setLoading(true)
        const data = await api.get<{ lessons: Lesson[] }>('/api/lessons')
        setLessons(data.lessons)
      } catch (e) {
        setError('Failed to load lessons')
      } finally {
        setLoading(false)
      }
    }
    fetchLessons()
  }, [])

  const filteredLessons = lessons.filter(
    (l) => l.title.toLowerCase().includes(search.toLowerCase()) ||
           l.description.toLowerCase().includes(search.toLowerCase()) ||
           l.category.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '300px' }}>
        <div style={{ color: 'var(--color-text-muted)' }}>Loading lessons…</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <p style={{ color: 'var(--color-danger)', marginBottom: '1rem' }}>{error}</p>
        <button className="btn btn-primary" onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    )
  }

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>Lessons</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Visual, example-driven guide to Claude Code — from basic concepts to advanced agents.</p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <input
          type="search"
          className="input"
          placeholder="Search lessons by title, description, or category…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ maxWidth: '400px' }}
        />
      </div>

      {filteredLessons.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: 'var(--color-text-muted)', marginBottom: '1rem' }}>
            {search ? 'No lessons match your search.' : 'No lessons available yet. Check back soon!'}
          </p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.5rem' }}>
          {filteredLessons.map((lesson) => (
            <Link to={`/lessons/${lesson.id}`} key={lesson.id} style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%', transition: 'transform var(--transition), box-shadow var(--transition)', borderColor: 'var(--color-border)' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span className={`badge badge-${lesson.difficulty === 'beginner' ? 'success' : lesson.difficulty === 'intermediate' ? 'warning' : 'danger'}`}>
                    {lesson.difficulty}
                  </span>
                  <span className="badge badge-primary">{lesson.category}</span>
                </div>
                <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '0.5rem' }}>{lesson.title}</h3>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem', marginBottom: '1rem', flex: 1 }}>{lesson.description}</p>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
                  <span>⏱ {lesson.estimated_minutes} min</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}