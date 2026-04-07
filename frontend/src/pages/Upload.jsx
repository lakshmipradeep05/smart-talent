import { useState } from 'react'
import { uploadResumes } from '../api'

export default function Upload() {
  const [files, setFiles]       = useState([])
  const [jobRole, setJobRole]   = useState('')
  const [loading, setLoading]   = useState(false)
  const [result, setResult]     = useState(null)
  const [error, setError]       = useState('')

  const handleSubmit = async () => {
    if (!files.length || !jobRole) {
      setError('Please select files and enter a job role.')
      return
    }
    setError('')
    setLoading(true)

    const formData = new FormData()
    formData.append('job_role', jobRole)
    Array.from(files).forEach(f => formData.append('files', f))

    try {
      const res = await uploadResumes(formData)
      setResult(res.data)
    } catch (e) {
      setError('Upload failed. Make sure the backend is running.')
    }
    setLoading(false)
  }

  return (
    <div>
      <h2 className="page-title">📁 Upload Resumes</h2>

      <div className="card" style={{maxWidth: 600}}>

        {error && <div className="alert error">{error}</div>}
        {result && (
          <div className="alert success">
            ✅ {result.successful} uploaded successfully, {result.failed} failed.
          </div>
        )}

        <div className="form-group">
          <label>Job Role</label>
          <input
            type="text"
            placeholder="e.g. Python ML Developer"
            value={jobRole}
            onChange={e => setJobRole(e.target.value)}
          />
        </div>

        <div
          className="upload-box"
          onClick={() => document.getElementById('fileInput').click()}
        >
          <div style={{fontSize: 40}}>📄</div>
          <p>Click to select resumes (PDF or DOCX)</p>
          {files.length > 0 && (
            <p style={{color: '#4f46e5', marginTop: 8}}>
              {files.length} file(s) selected
            </p>
          )}
          <input
            id="fileInput"
            type="file"
            multiple
            accept=".pdf,.docx"
            style={{display: 'none'}}
            onChange={e => setFiles(e.target.files)}
          />
        </div>

        <button
          className="btn btn-primary"
          style={{marginTop: 20, width: '100%'}}
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? 'Uploading...' : 'Upload Resumes'}
        </button>

        {/* Show results per file */}
        {result && (
          <table style={{marginTop: 24}}>
            <thead>
              <tr><th>Filename</th><th>Status</th></tr>
            </thead>
            <tbody>
              {result.results.map((r, i) => (
                <tr key={i}>
                  <td>{r.filename}</td>
                  <td style={{color: r.status === 'success' ? 'green' : 'red'}}>
                    {r.status}
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