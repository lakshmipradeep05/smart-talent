import { useEffect, useState } from 'react'
import { getDashboard } from '../api'

export default function Dashboard() {
  const [data, setData] = useState(null)

  useEffect(() => {
    getDashboard().then(res => setData(res.data))
  }, [])

  if (!data) return <p>Loading...</p>

  return (
    <div>
      <h2 className="page-title">📊 Recruiter Dashboard</h2>

      {/* Stats row */}
      <div className="stats-row">
        <div className="stat-card">
          <h2>{data.total_resumes}</h2>
          <p>Total Resumes</p>
        </div>
        <div className="stat-card">
          <h2>{data.total_jobs}</h2>
          <p>Active Jobs</p>
        </div>
        <div className="stat-card">
          <h2>{Object.keys(data.resumes_by_role).length}</h2>
          <p>Roles Hiring</p>
        </div>
      </div>

      {/* Top talent preview */}
      <div className="card">
        <h3 style={{marginBottom: 16}}>⭐ Top Talent Preview</h3>
        {data.top_talent.length === 0 ? (
          <p style={{color: '#718096'}}>No resumes uploaded yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Experience</th>
                <th>Top Skills</th>
              </tr>
            </thead>
            <tbody>
              {data.top_talent.map((t, i) => (
                <tr key={i}>
                  <td>{t.name}</td>
                  <td>{t.role}</td>
                  <td>{t.experience_years} yrs</td>
                  <td>
                    {t.top_skills.map(s => (
                      <span key={s} className="skill-tag">{s}</span>
                    ))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}