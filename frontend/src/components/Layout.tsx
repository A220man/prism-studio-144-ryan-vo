import { NavLink, Outlet } from 'react-router-dom'

export function Layout() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <header
        style={{
          background: 'var(--color-bg-secondary)',
          borderBottom: '1px solid var(--color-border)',
          padding: '1rem 0',
          position: 'sticky',
          top: 0,
          zIndex: 100,
        }}
      >
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem' }}>
          <NavLink to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 700, fontSize: '1.25rem', color: 'var(--color-text)' }}>
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', width: 36, height: 36, borderRadius: 'var(--radius)', background: 'linear-gradient(135deg, var(--color-primary), #a855f7)' }}>
              △
            </span>
            Prism Studio
          </NavLink>
          <nav style={{ display: 'flex', gap: '0.5rem' }}>
            <NavLink
              to="/"
              style={({ isActive }) => ({
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius)',
                fontWeight: 500,
                color: isActive ? 'var(--color-primary)' : 'var(--color-text-muted)',
                background: isActive ? 'rgba(88, 166, 255, 0.1)' : 'transparent',
              })}
            >
              Lessons
            </NavLink>
            <NavLink
              to="/workflows"
              style={({ isActive }) => ({
                padding: '0.5rem 1rem',
                borderRadius: 'var(--radius)',
                fontWeight: 500,
                color: isActive ? 'var(--color-primary)' : 'var(--color-text-muted)',
                background: isActive ? 'rgba(88, 166, 255, 0.1)' : 'transparent',
              })}
            >
              Workflows
            </NavLink>
          </nav>
        </div>
      </header>
      <main style={{ flex: 1, padding: '2rem 0' }}>
        <div className="container">
          <Outlet />
        </div>
      </main>
      <footer
        style={{
          background: 'var(--color-bg-secondary)',
          borderTop: '1px solid var(--color-border)',
          padding: '1.5rem 0',
          marginTop: 'auto',
        }}
      >
        <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
            Prism Studio — Visual, example-driven guide to Claude Code
          </p>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>
            Ryan Vo | AI & Machine Learning &nbsp;•&nbsp; ryandtvo@gmail.com
          </p>
        </div>
      </footer>
    </div>
  )
}