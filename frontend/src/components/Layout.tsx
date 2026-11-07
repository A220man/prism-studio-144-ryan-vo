import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'

export function Layout() {
  const { user, loading, login, logout } = useAuth()

  if (loading) {
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
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ width: '100px', height: '36px', background: 'var(--color-bg-tertiary)', borderRadius: 'var(--radius)', animation: 'pulse 1.5s ease-in-out infinite' }} />
            </div>
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
          <nav style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
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
            {user ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginLeft: '1rem', paddingLeft: '1rem', borderLeft: '1px solid var(--color-border)' }}>
                <span style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>
                  {user.sub}
                  {user.roles.length > 0 && (
                    <>
                      {' '}
                      {user.roles.map((r) => (
                        <span key={r} style={{ marginLeft: '0.25rem', padding: '0.125rem 0.5rem', borderRadius: 'var(--radius)', background: 'var(--color-primary)', color: 'white', fontSize: '0.7rem', fontWeight: 600, textTransform: 'uppercase' }}>
                          {r}
                        </span>
                      ))}
                    </>
                  )}
                </span>
                <button
                  onClick={logout}
                  style={{
                    padding: '0.5rem 1rem',
                    borderRadius: 'var(--radius)',
                    fontWeight: 500,
                    color: 'var(--color-text)',
                    background: 'var(--color-bg-tertiary)',
                    border: '1px solid var(--color-border)',
                    cursor: 'pointer',
                  }}
                >
                  Logout
                </button>
              </div>
            ) : (
              <button
                onClick={login}
                style={{
                  padding: '0.5rem 1rem',
                  borderRadius: 'var(--radius)',
                  fontWeight: 600,
                  color: 'white',
                  background: 'var(--color-primary)',
                  border: 'none',
                  cursor: 'pointer',
                }}
              >
                Sign In
              </button>
            )}
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