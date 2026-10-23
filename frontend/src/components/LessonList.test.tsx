import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { LessonList } from '@/components/LessonList'
import { Workflows } from '@/components/Workflows'
import { api } from '@/api/client'

// Mock the API client
vi.mock('@/api/client', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>)
}

describe('LessonList', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows loading state initially', () => {
    api.get.mockResolvedValue({ lessons: [], total: 0, page: 1, page_size: 20 })

    renderWithRouter(<LessonList />)

    expect(screen.getByText('Loading lessons…')).toBeInTheDocument()
  })

  it('displays lessons when loaded', async () => {
    const mockLessons = [
      {
        id: 'cli-basics',
        title: 'CLI Basics',
        description: 'Learn the fundamental commands',
        category: 'Fundamentals',
        difficulty: 'beginner' as const,
        estimated_minutes: 15,
      },
    ]
    api.get.mockResolvedValue({ lessons: mockLessons, total: 1, page: 1, page_size: 20 })

    renderWithRouter(<LessonList />)

    await waitFor(() => {
      expect(screen.getByText('CLI Basics')).toBeInTheDocument()
    })
    expect(screen.getByText('Fundamentals')).toBeInTheDocument()
    expect(screen.getByText((content) => content.includes('15') && content.includes('min'))).toBeInTheDocument()
  })
})

describe('Workflows', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders workflow sidebar', () => {
    renderWithRouter(<Workflows />)

    expect(screen.getByText('Skill Creation Wizard')).toBeInTheDocument()
    expect(screen.getByText('Subagent Builder')).toBeInTheDocument()
    expect(screen.getByText('MCP Server Configurator')).toBeInTheDocument()
  })

  it('shows skill wizard form when selected', () => {
    renderWithRouter(<Workflows />)

    // Use the first matching element (sidebar button)
    const buttons = screen.getAllByText('Skill Creation Wizard')
    fireEvent.click(buttons[0])

    expect(screen.getByLabelText('Skill Name')).toBeInTheDocument()
    expect(screen.getByLabelText('Description')).toBeInTheDocument()
    expect(screen.getByLabelText('Model')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Generate Skill' })).toBeInTheDocument()
  })

  it('generates skill template on submit', async () => {
    api.post.mockResolvedValue('name: test-skill\ndescription: A test skill\nmodel: sonnet')

    renderWithRouter(<Workflows />)

    const buttons = screen.getAllByText('Skill Creation Wizard')
    fireEvent.click(buttons[0])

    fireEvent.change(screen.getByLabelText('Skill Name'), { target: { value: 'test-skill' } })
    fireEvent.change(screen.getByLabelText('Description'), { target: { value: 'A test skill' } })

    fireEvent.click(screen.getByRole('button', { name: 'Generate Skill' }))

    await waitFor(() => {
      expect(screen.getByText((content) => content.includes('name:') && content.includes('test-skill'))).toBeInTheDocument()
    })
  })
})