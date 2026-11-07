import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from '@/context/AuthContext'
import { LessonList } from '@/components/LessonList'
import { LessonDetail } from '@/components/LessonDetail'
import { Workflows } from '@/components/Workflows'
import { Callback } from '@/components/Callback'
import { Layout } from '@/components/Layout'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<LessonList />} />
          <Route path="/lessons/:id" element={<LessonDetail />} />
          <Route path="/workflows" element={<Workflows />} />
          <Route path="/callback" element={<Callback />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App