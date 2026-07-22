import { Navigate, Route, Routes } from 'react-router-dom'
import { UserDetailPage } from './pages/UserDetailPage'
import { UsersListPage } from './pages/UsersListPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/users" replace />} />
      <Route path="/users" element={<UsersListPage />} />
      <Route path="/users/:id" element={<UserDetailPage />} />
    </Routes>
  )
}

export default App
