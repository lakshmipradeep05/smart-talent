import { useState, useEffect } from 'react'
import { createJob, rankCandidates, getJobs } from '../api'

export default function Ranking() {
  const [jobs, setJobs]           = useState([])
  const [title, setTitle]         = useState('')
  const [description, setDesc]    = useState('')
  const [results, setResults]     = useState(null)
  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState('')

  useEffect(() => {
    getJobs().then(res => setJobs(res.data))
  }, [])

  const handleRank = async () => {
    if (!title || !description) {
      setError('Please fill in job title and description.')
      return
    }
    setError('')
    setLoading(true)
    try {
      const jobRes = await createJob({ title, description,
        required_skills: [], min_experience_years: 0 })
      const rankRes = await rankCandidates(jobRes.data.id)
      setResults(rankRes.data)
      setJobs(prev => [...prev, jobRes.data])
    } catch (e) {
      setError('Ranking failed. Make sure resumes are uploaded.')
    }
    setLoading(false)
  }

  const scoreClass = (score) => {
    if (score >= 70) return 'high'
    if (score >= 40) return 'medium'
    return 'low'
  }

  return (
    <div>
      <h2 className="page-title">🏆 Rank Candidates</h2>

      {/* Job form */}
      <div className="card" style={{maxWidth: 600, marginBottom: 32}}>
        {error && <div className="alert error">{error}</div>}

        <div className="form-group">
          <label>Job Title</label>
          <input
            type="text"
            placeholder="e.g. Python ML Developer"
            value={title}
            onChange={e => setTitle(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Job Description</label>
          <textarea
            rows={5}
            placeholder="Paste the full job description here..."
            value={description}
            onChange={e => setDesc(e.target.value)}
          />
        </div>

        <button
          className="btn btn-primary"
          onClick={handleRank}
          disabled={loading}
        >
          {loading ? 'Ranking...' : '🚀 Rank Candidates'}
        </button>
      </div>

      {/* Results table */}
      {results && (
        <div className="card">
          <h3 style={{marginBottom: 16}}>
            Results for "{results.job_title}" — {results.total_candidates} candidates
          </h3>
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Candidate</th>
                <th>Score</th>
                <th>Experience</th>
                <th>Top Skills</th>
                <th>Why Ranked</th>
              </tr>
            </thead>
            <tbody>
              {results.ranked_candidates.map(c => (
                <tr key={c.resume_id}>
                  <td>#{c.rank}</td>
                  <td>{c.candidate_name}</td>
                  <td>
                    <span className={`score ${scoreClass(c.compatibility_score)}`}>
                      {c.compatibility_score}%
                    </span>
                  </td>
                  <td>{c.total_experience_years} yrs</td>
                  <td>
                    {c.top_skills.map(s => (
                      <span key={s} className="skill-tag">{s}</span>
                    ))}
                  </td>
                  <td>
                    {c.ai_justification
                      ? <div className="justification">{c.ai_justification}</div>
                      : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}