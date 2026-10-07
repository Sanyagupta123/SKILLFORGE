const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export async function analyzeJob({ jobDescription, resume }) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ job_description: jobDescription, resume }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Unable to connect to the analysis service. Please try again.');
  }

  return data;
}

export async function fetchAnalyses() {
  const response = await fetch(`${API_BASE_URL}/analyses`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error('Unable to load previous analyses.');
  }
  return data;
}
