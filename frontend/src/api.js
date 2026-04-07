import axios from 'axios'

// All API calls go to your FastAPI backend
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

export const getDashboard   = ()           => api.get('/dashboard')
export const getResumes     = ()           => api.get('/resumes/')
export const uploadResumes  = (formData)   => api.post('/resumes/upload', formData)
export const createJob      = (jobData)    => api.post('/jobs/', jobData)
export const rankCandidates = (jobId)      => api.post(`/jobs/${jobId}/rank`)
export const getJobs        = ()           => api.get('/jobs/')