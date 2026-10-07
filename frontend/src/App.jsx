import { useEffect, useMemo, useState } from 'react';
import { analyzeJob, fetchAnalyses } from './services/api';

const defaultForm = {
  jobDescription: '',
  resume: '',
};

function App() {
  const [form, setForm] = useState(defaultForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await fetchAnalyses();
      setHistory(data);
    } catch (historyError) {
      setHistory([]);
    }
  };

  const categoryEntries = useMemo(() => {
    if (!result || !result.categories) return [];
    return Object.entries(result.categories).map(([label, value]) => ({
      label,
      value,
    }));
  }, [result]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleAnalyze = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await analyzeJob({
        jobDescription: form.jobDescription,
        resume: form.resume,
      });
      setResult(data);
      await loadHistory();
    } catch (submitError) {
      setError(submitError.message || 'Unable to connect to the analysis service. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Career intelligence</p>
          <h1>SkillForge</h1>
        </div>
        <div className="topbar-copy">Understand your job skill gap. Build your career smarter.</div>
      </header>

      <main className="dashboard">
        <section className="panel form-panel">
          <div className="panel-header">
            <h2>Analyze your fit</h2>
          </div>

          <form onSubmit={handleAnalyze} className="analysis-form">
            <label className="field">
              <span>Job Description</span>
              <textarea
                name="jobDescription"
                value={form.jobDescription}
                onChange={handleChange}
                placeholder="Paste the job description..."
                rows="8"
              />
            </label>

            <label className="field">
              <span>Your Resume</span>
              <textarea
                name="resume"
                value={form.resume}
                onChange={handleChange}
                placeholder="Paste your resume or experience summary..."
                rows="8"
              />
            </label>

            <button type="submit" disabled={loading} className="primary-button">
              {loading ? 'Analyzing your job...' : 'Analyze Job'}
            </button>
          </form>

          {error && <div className="error-box">{error}</div>}
        </section>

        <aside className="panel history-panel">
          <div className="panel-header">
            <h2>Previous Analyses</h2>
          </div>

          {history.length === 0 ? (
            <p className="empty-text">No saved analyses yet.</p>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <div className="history-item" key={item.id}>
                  <div className="history-topline">
                    <strong>{item.job_description.slice(0, 30) || 'Analysis'}...</strong>
                    <span>{item.match_score}%</span>
                  </div>
                  <small>{new Date(item.created_at).toLocaleDateString()}</small>
                </div>
              ))}
            </div>
          )}
        </aside>
      </main>

      <section className="results panel">
        {loading && (
          <div className="loading-state">
            <div className="spinner" />
            <p>Analyzing your job...</p>
          </div>
        )}

        {!loading && !result && !error && (
          <div className="empty-state">
            <h3>Your result will appear here</h3>
            <p>Paste a job description and resume to compare your skills against the role.</p>
          </div>
        )}

        {!loading && result && (
          <>
            <div className="result-header">
              <div>
                <p className="eyebrow">Your result</p>
                <h2>{result.score.toFixed(2)}%</h2>
              </div>
              <div className="score-badge">Match Score</div>
            </div>

            <div className="results-grid">
              <div className="result-card">
                <h3>Matched Skills</h3>
                <ul className="skill-list">
                  {result.matched.length === 0 ? <li className="muted">No matching skills detected.</li> : result.matched.map((skill) => <li key={skill}>✓ {skill}</li>)}
                </ul>
              </div>

              <div className="result-card">
                <h3>Skill Gap</h3>
                <ul className="skill-list gap-list">
                  {result.missing.length === 0 ? <li className="muted">No skill gaps detected.</li> : result.missing.map((skill) => <li key={skill}>✕ {skill}</li>)}
                </ul>
              </div>
            </div>

            {categoryEntries.length > 0 && (
              <div className="category-section">
                <h3>Category Coverage</h3>
                <div className="category-grid">
                  {categoryEntries.map(({ label, value }) => (
                    <div className="category-card" key={label}>
                      <div className="category-header">
                        <span>{label}</span>
                        <strong>{value}%</strong>
                      </div>
                      <div className="progress-track">
                        <span style={{ width: `${value}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.recommendations && result.recommendations.length > 0 && (
              <div className="recommendations">
                <h3>Recommended next steps</h3>
                <div className="recommendation-list">
                  {result.recommendations.map((item) => (
                    <div className="recommendation-item" key={item.skill}>
                      <div className="recommendation-title">{item.skill}</div>
                      <ul>
                        {item.recommendations.map((tip) => <li key={tip}>{tip}</li>)}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </section>
    </div>
  );
}

export default App;
