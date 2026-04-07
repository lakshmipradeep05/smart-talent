import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Ranking from './pages/Ranking'

function App() {
  return (
    <BrowserRouter>
      <div className="layout">

        {/* Sidebar navigation */}
        <aside className="sidebar">
          <h1>🎯 Smart Talent</h1>
          <NavLink to="/"        end>📊 Dashboard</NavLink>
          <NavLink to="/upload"     >📁 Upload Resumes</NavLink>
          <NavLink to="/ranking"    >🏆 Rank Candidates</NavLink>
        </aside>

        {/* Page content */}
        <main className="main">
          <Routes>
            <Route path="/"        element={<Dashboard />} />
            <Route path="/upload"  element={<Upload />}    />
            <Route path="/ranking" element={<Ranking />}   />
          </Routes>
        </main>

      </div>
    </BrowserRouter>
  )
}

export default App