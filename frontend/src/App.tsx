import { Routes, Route } from 'react-router-dom'
import { LessonList } from '@/components/LessonList'
import { LessonDetail } from '@/components/LessonDetail'
import { Workflows } from '@/components/Workflows'
import { Layout } from '@/components/Layout'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<LessonList />} />
        <Route path="/lessons/:id" element={<LessonDetail />} />
        <Route path="/workflows" element={<Workflows />} />
      </Route>
    </Routes>
  )
}

export default App