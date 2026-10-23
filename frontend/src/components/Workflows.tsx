import { useState, FormEvent } from 'react'
import { api } from '@/api/client'

interface Workflow {
  id: string
  title: string
  description: string
  icon: string
}

const WORKFLOWS: Workflow[] = [
  {
    id: 'skill-wizard',
    title: 'Skill Creation Wizard',
    description: 'Generate a complete .claude/skills/ YAML file with proper frontmatter, tools, and examples.',
    icon: '⚙️',
  },
  {
    id: 'subagent-builder',
    title: 'Subagent Builder',
    description: 'Create a specialized subagent with model selection, tools, and system prompt template.',
    icon: '🤖',
  },
  {
    id: 'mcp-configurator',
    title: 'MCP Server Configurator',
    description: 'Configure Model Context Protocol servers with transport, auth, and capability settings.',
    icon: '🔌',
  },
]

interface SkillWizardFormProps {
  onGenerate: (data: Record<string, string>) => void
  loading: boolean
}

function SkillWizardForm({ onGenerate, loading }: SkillWizardFormProps) {
  const [form, setForm] = useState({
    name: '',
    description: '',
    model: 'sonnet',
    tools: 'bash,read,write,edit,glob,grep,task',
    allowed_tools: '',
    example: 'do something',
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onGenerate(form)
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div>
        <label htmlFor="skill-name" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Skill Name</label>
        <input id="skill-name" className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="my-skill" required />
      </div>
      <div>
        <label htmlFor="skill-description" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Description</label>
        <textarea id="skill-description" className="input" rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="What does this skill do?" required />
      </div>
      <div>
        <label htmlFor="skill-model" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Model</label>
        <select id="skill-model" className="input" value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })}>
          <option value="sonnet">Claude 3.5 Sonnet</option>
          <option value="opus">Claude 3 Opus</option>
          <option value="haiku">Claude 3.5 Haiku</option>
        </select>
      </div>
      <div>
        <label htmlFor="skill-tools" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Tools (comma-separated)</label>
        <input id="skill-tools" className="input" value={form.tools} onChange={(e) => setForm({ ...form, tools: e.target.value })} placeholder="bash,read,write,edit,glob,grep,task" />
      </div>
      <div>
        <label htmlFor="skill-allowed-tools" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Allowed Tools (comma-separated, optional)</label>
        <input id="skill-allowed-tools" className="input" value={form.allowed_tools} onChange={(e) => setForm({ ...form, allowed_tools: e.target.value })} placeholder="bash,read" />
      </div>
      <div>
        <label htmlFor="skill-example" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Example Usage</label>
        <textarea id="skill-example" className="input" rows={4} value={form.example} onChange={(e) => setForm({ ...form, example: e.target.value })} placeholder="/my-skill do something" />
      </div>
      <button className="btn btn-primary" type="submit" disabled={loading}>
        {loading ? 'Generating…' : 'Generate Skill'}
      </button>
    </form>
  )
}

interface SubagentBuilderFormProps {
  onGenerate: (data: Record<string, string>) => void
  loading: boolean
}

function SubagentBuilderForm({ onGenerate, loading }: SubagentBuilderFormProps) {
  const [form, setForm] = useState({
    name: '',
    description: '',
    model: 'sonnet',
    tools: 'bash,read,write,edit,glob,grep,task',
    system_prompt: '',
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onGenerate(form)
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div>
        <label htmlFor="agent-name" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Agent Name</label>
        <input id="agent-name" className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="code-reviewer" required />
      </div>
      <div>
        <label htmlFor="agent-description" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Description</label>
        <textarea id="agent-description" className="input" rows={3} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} placeholder="What does this agent do?" required />
      </div>
      <div>
        <label htmlFor="agent-model" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Model</label>
        <select id="agent-model" className="input" value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })}>
          <option value="sonnet">Claude 3.5 Sonnet</option>
          <option value="opus">Claude 3 Opus</option>
          <option value="haiku">Claude 3.5 Haiku</option>
        </select>
      </div>
      <div>
        <label htmlFor="agent-tools" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Tools (comma-separated)</label>
        <input id="agent-tools" className="input" value={form.tools} onChange={(e) => setForm({ ...form, tools: e.target.value })} placeholder="bash,read,write,edit,glob,grep,task" />
      </div>
      <div>
        <label htmlFor="agent-system-prompt" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>System Prompt</label>
        <textarea id="agent-system-prompt" className="input" rows={6} value={form.system_prompt} onChange={(e) => setForm({ ...form, system_prompt: e.target.value })} placeholder="You are a specialized agent that…" required />
      </div>
      <button className="btn btn-primary" type="submit" disabled={loading}>
        {loading ? 'Generating…' : 'Generate Subagent'}
      </button>
    </form>
  )
}

interface MCPConfiguratorFormProps {
  onGenerate: (data: Record<string, string>) => void
  loading: boolean
}

function MCPConfiguratorForm({ onGenerate, loading }: MCPConfiguratorFormProps) {
  const [form, setForm] = useState({
    name: '',
    command: '',
    args: '',
    env: '',
    transport: 'stdio',
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onGenerate(form)
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div>
        <label htmlFor="mcp-name" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Server Name</label>
        <input id="mcp-name" className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="filesystem" required />
      </div>
      <div>
        <label htmlFor="mcp-transport" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Transport</label>
        <select id="mcp-transport" className="input" value={form.transport} onChange={(e) => setForm({ ...form, transport: e.target.value })}>
          <option value="stdio">stdio (local process)</option>
          <option value="sse">SSE (remote)</option>
        </select>
      </div>
      <div>
        <label htmlFor="mcp-command" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Command</label>
        <input id="mcp-command" className="input" value={form.command} onChange={(e) => setForm({ ...form, command: e.target.value })} placeholder="npx" required />
      </div>
      <div>
        <label htmlFor="mcp-args" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Arguments (space-separated)</label>
        <input id="mcp-args" className="input" value={form.args} onChange={(e) => setForm({ ...form, args: e.target.value })} placeholder="-y @modelcontextprotocol/server-filesystem /path/to/dir" />
      </div>
      <div>
        <label htmlFor="mcp-env" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Environment Variables (JSON, optional)</label>
        <textarea id="mcp-env" className="input" rows={3} value={form.env} onChange={(e) => setForm({ ...form, env: e.target.value })} placeholder='{"API_KEY": "value"}' />
      </div>
      <button className="btn btn-primary" type="submit" disabled={loading}>
        {loading ? 'Generating…' : 'Generate MCP Config'}
      </button>
    </form>
  )
}

export function Workflows() {
  const [activeWorkflow, setActiveWorkflow] = useState<string | null>(null)
  const [generated, setGenerated] = useState<string>('')
  const [copied, setCopied] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleGenerate = async (workflowId: string, formData: Record<string, string>) => {
    setLoading(true)
    try {
      const response = await api.post<string>(`/api/workflows/${workflowId}`, formData)
      setGenerated(response)
    } catch (e) {
      setGenerated('Error generating template. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const copyOutput = async () => {
    await navigator.clipboard.writeText(generated)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>Interactive Workflows</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Generate copy-paste templates for common Claude Code configurations — no LLM required.</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr', gap: '2rem' }}>
        <aside style={{ position: 'sticky', top: '100px', height: 'fit-content' }}>
          <div className="card">
            <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem' }}>Workflows</h3>
            <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {WORKFLOWS.map((wf) => (
                <button
                  key={wf.id}
                  onClick={() => { setActiveWorkflow(wf.id); setGenerated(''); }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    width: '100%',
                    padding: '0.75rem 1rem',
                    borderRadius: 'var(--radius)',
                    textAlign: 'left',
                    background: activeWorkflow === wf.id ? 'rgba(88, 166, 255, 0.15)' : 'transparent',
                    border: activeWorkflow === wf.id ? '1px solid var(--color-primary)' : '1px solid transparent',
                    color: activeWorkflow === wf.id ? 'var(--color-primary)' : 'var(--color-text)',
                    fontWeight: activeWorkflow === wf.id ? 600 : 400,
                    transition: 'all var(--transition)',
                  }}
                >
                  <span style={{ fontSize: '1.25rem' }}>{wf.icon}</span>
                  <div>
                    <div style={{ fontWeight: 500 }}>{wf.title}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>{wf.description}</div>
                  </div>
                </button>
              ))}
            </nav>
          </div>
        </aside>

        <div>
          {activeWorkflow === 'skill-wizard' && <div className="card"><SkillWizardForm onGenerate={(data) => handleGenerate('skill-wizard', data)} loading={loading} /></div>}
          {activeWorkflow === 'subagent-builder' && <div className="card"><SubagentBuilderForm onGenerate={(data) => handleGenerate('subagent-builder', data)} loading={loading} /></div>}
          {activeWorkflow === 'mcp-configurator' && <div className="card"><MCPConfiguratorForm onGenerate={(data) => handleGenerate('mcp-configurator', data)} loading={loading} /></div>}
          {!activeWorkflow && (
            <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
              <p style={{ color: 'var(--color-text-muted)', marginBottom: '1rem' }}>Select a workflow from the sidebar to get started.</p>
            </div>
          )}

          {generated && (
            <div className="card" style={{ marginTop: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Generated Output</h3>
                <button className="btn btn-secondary" onClick={copyOutput} style={{ fontSize: '0.75rem' }}>
                  {copied ? '✓ Copied' : 'Copy to Clipboard'}
                </button>
              </div>
              <pre style={{ maxHeight: '400px', overflow: 'auto' }}><code>{generated}</code></pre>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}