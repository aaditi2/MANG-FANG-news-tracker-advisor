import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedCompany, setSelectedCompany] = useState('Apple');
  const [newsType, setNewsType] = useState('Top');
  const [timeRange, setTimeRange] = useState('Past Day');
  const [news, setNews] = useState([]);
  const [suggestions, setSuggestions] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGetNews = async () => {
    setLoading(true);
    setSuggestions('');
    try {
      const response = await axios.get(`http://localhost:8000/get_news/${selectedCompany}`, {
        params: {
          category: newsType,
          timeframe: timeRange
        }
      });
      setNews(response.data.news || []);
      try {
        setSuggestions(JSON.parse(response.data.suggestions));
      } catch (e) {
        console.error("Suggestion JSON parse failed:", e);
        setSuggestions([]);
      }
    } catch (error) {
      console.error("Error fetching news:", error);
      setNews([]);
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: 'Segoe UI, sans-serif', backgroundColor: '#fafafa', padding: '30px' }}>
      <h1>📊 Company Strategy Advisor</h1>

      <div style={{ marginBottom: '20px' }}>
        <button onClick={handleGetNews} style={{
          padding: '8px 14px',
          fontSize: '16px',
          borderRadius: '6px',
          marginRight: '10px',
          cursor: 'pointer'
        }}>
          Get Latest News
        </button>

        <select value={selectedCompany} onChange={e => setSelectedCompany(e.target.value)} style={{ padding: '8px', fontSize: '16px', borderRadius: '6px' }}>
          <option>Apple</option>
          <option>Meta</option>
          <option>Google</option>
          <option>Amazon</option>
          <option>Netflix</option>
          <option>Microsoft</option>
          <option>Startup</option>
        </select>

        <select value={newsType} onChange={e => setNewsType(e.target.value)} style={{ padding: '8px', fontSize: '16px', borderRadius: '6px', marginLeft: '10px' }}>
          <option>Top</option>
          <option>Tech</option>
          <option>AI</option>
          <option>Finance</option>
        </select>

        <select value={timeRange} onChange={e => setTimeRange(e.target.value)} style={{ padding: '8px', fontSize: '16px', borderRadius: '6px', marginLeft: '10px' }}>
          <option>Today</option>
          <option>Past Week</option>
          <option>Past Month</option>
        </select>
      </div>

      {loading && <p>⌛ Loading...</p>}

      {Array.isArray(news) && news.length > 0 && (
        <div>
          <h2>📰 Competitor News</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {news.map((item, index) => (
              <div key={index} style={{
                backgroundColor: "#f2f2f2",
                padding: "10px",
                borderRadius: "8px",
                borderLeft: "5px solid #333"
              }}>
                <strong>{item.company}</strong>: {item.title}
                <a href={item.link} target="_blank" rel="noopener noreferrer" title="Open news article">
                  <svg className="link-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M10 13a5 5 0 0 0 7.07 0l3.54-3.54a5 5 0 0 0-7.07-7.07L12 4" />
                    <path d="M14 11a5 5 0 0 0-7.07 0L3.39 14.46a5 5 0 0 0 7.07 7.07L12 20" />
                  </svg>
                </a>
              </div>
            ))}
          </div>
        </div>
      )}

      {suggestions && Array.isArray(suggestions) && suggestions.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h2>📋 Structured Strategy Table</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
            <thead>
              <tr style={{ backgroundColor: '#ffe0b3' }}>
                <th style={{ border: '1px solid #ccc', padding: '10px' }}>Strategy</th>
                <th style={{ border: '1px solid #ccc', padding: '10px' }}>Objective</th>
                <th style={{ border: '1px solid #ccc', padding: '10px' }}>Action Items</th>
              </tr>
            </thead>
            <tbody>
              {suggestions.map((item, index) => (
                <tr key={index}>
                  <td style={{ border: '1px solid #ccc', padding: '10px' }}>{item.strategy}</td>
                  <td style={{ border: '1px solid #ccc', padding: '10px' }}>{item.objective}</td>
                  <td style={{ border: '1px solid #ccc', padding: '10px' }}>
                    <ul>
                      {item.actions.map((act, idx) => <li key={idx}>{act}</li>)}
                    </ul>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
