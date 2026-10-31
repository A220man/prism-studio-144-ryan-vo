
import { useState, useEffect, useCallback } from 'react'
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

const CATEGORIES = ['Fundamentals', 'Skills', 'Agents', 'Integrations', 'Advanced']
const DIFFICULTIES = ['beginner', 'intermediate', 'advanced'] as const

export function LessonList() {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState<string>('')
  const [difficulty, setDifficulty] = useState<'beginner' | 'intermediate' | 'advanced' | ''>('')
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const pageSize = 20

  const fetchLessons = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const params = new URLSearchParams()
      params.set('page', page.toString())
      params.set('page_size', pageSize.toString())
      if (search) params.set('search', search)
      if (category) params.set('category', category)
      if (difficulty) params.set('difficulty', difficulty)
      const data = await api.get<{ lessons: Lesson[]; total: number; page: number; page_size: number }>(`/api/lessons?${params.toString()}`)
      setLessons(data.lessons)
      setTotal(data.total)
    } catch (e) {
      setError('Failed to load lessons')
    } finally {
      setLoading(false)
    }
  }, [page, search, category, difficulty])

  useEffect(() => {
    fetchLessons()
  }, [fetchLessons])

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value)
    setPage(1)
  }

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCategory(e.target.value)
    setPage(1)
  }

  const handleDifficultyChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setDifficulty(e.target.value as 'beginner' | 'intermediate' | 'advanced' | '')
    setPage(1)
  }

  const handlePageChange = (newPage: number) => {
    setPage(newPage)
  }

  const totalPages = Math.ceil(total / pageSize)

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
        <div style={{ color: 'var(--color-error)', marginBottom: '1rem' }}>Failed to load lessons</div>
        <button onClick={fetchLessons} style={{ padding: '0.5rem 1rem' }}>Retry</button>
      </div>
    )
  }

  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem', alignItems: 'center' }}>
        <div style={{ flex: 1, minWidth: '200px' }}>
          <input
            type="text"
            placeholder="Search lessons…"
            value={search}
            onChange={handleSearchChange}
            style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--color-border)', background: 'var(--color-bg)', color: 'var(--color-text)' }}
          />
        </div>
        <div style={{ minWidth: '180px' }}>
          <select
            value={category}
            onChange={handleCategoryChange}
            style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--color-border)', background: 'var(--color-bg)', color: 'var(--color-text)' }}
          >
            <option value="">All Categories</option>
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div style={{ minWidth: '180px' }}>
          <select
            value={difficulty}
            onChange={handleDifficultyChange}
            style={{ width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--color-border)', background: 'var(--color-bg)', color: 'var(--color-text)' }}
          >
            <option value="">All Difficulties</option>
            {DIFFICULTIES.map((diff) => (
              <option key={diff} value={diff}>{diff.charAt(0).toUpperCase() + diff.slice(1)}</option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))' }}>
        {lessons.map((lesson) => (
          <Link to={`/lessons/${lesson.id}`} key={lesson.id} style={{ textDecoration: 'none', color: 'inherit' }}>
            <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
              <div style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
                  <span className="badge" style={{ background: 'var(--color-primary-bg)', color: 'var(--color-primary)', textTransform: 'capitalize' }}>
                    {lesson.category}
                  </span>
                  <span className="badge" style={{ background: 'var(--color-secondary-bg)', color: 'var(--color-secondary)', textTransform: 'capitalize' }}>
                    {lesson.difficulty}
                  </span>
                </div>
                <h3 style={{ margin: '0 0 0.5rem', fontSize: '1.125rem' }}>{lesson.title}</h3>
                <p style={{ margin: 0, color: 'var(--color-text-muted)', fontSize: '0.875rem', lineHeight: 1.5 }}>
                  {lesson.description}
                </p>
              </div>
              <div style={{ padding: '0 1.5rem 1.5rem', marginTop: 'auto' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                  ~{lesson.estimated_minutes} min read
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem', marginTop: '2rem' }}>
          <button
            onClick={() => handlePageChange(page - 1)}
            disabled={page === 1}
            style={{ padding: '0.5rem 1rem', borderRadius: '4px', border: '1px solid var(--color-border)', background: 'var(--color-bg)', color: 'var(--color-text)', cursor: page === 1 ? 'not-allowed' : 'pointer' }}
          >
            Previous
          </button>
          <span style={{ color: 'var(--color-text-muted)' }}>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => handlePageChange(page + 1)}
            disabled={page === totalPages}
            style={{ padding: '0.5rem 1rem', borderRadius: '4px', border: '1px solid var(--color-border)', background: 'var(--color-bg)', color: 'var(--color-text)', cursor: page === totalPages ? 'not-allowed' : 'pointer' }}
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

