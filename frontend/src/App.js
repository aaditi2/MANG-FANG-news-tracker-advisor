import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedCompany, setSelectedCompany] = useState('Apple');
  const [news, setNews] = useState('');
  const [suggestions, setSuggestions] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGetNews = async () => {
    setLoading(true);
    setSuggestions('');
    try {
      const response = await axios.get(`http://localhost:8000/get_news/${selectedCompany}`);
      setNews(response.data.news);
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error("Error fetching news:", error);
      setNews("⚠️ Failed to fetch news.");
      setSuggestions('');
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

        <select value={selectedCompany} onChange={e => setSelectedCompany(e.target.value)} style={{
          padding: '8px',
          fontSize: '16px',
          borderRadius: '6px'
        }}>
          <option>Apple</option>
          <option>Meta</option>
          <option>Google</option>
          <option>Amazon</option>
          <option>Netflix</option>
          <option>Microsoft</option>
          <option>Startup</option>
        </select>
      </div>

      {loading && <p>⌛ Loading...</p>}

      {news && (
        <div>
          <h2>📰 Competitor News</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {news.split('\n').map((line, index) => {
              const match = line.match(/- (.*?):/);
              const company = match ? match[1] : "Unknown";
              const headline = line.replace(/- .*?:\s*/, '');
              return (
                <div key={index} style={{
                  backgroundColor: "#f2f2f2",
                  padding: "10px",
                  borderRadius: "8px",
                  borderLeft: "5px solid #333"
                }}>
                  <strong>{company}</strong>: {headline}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {suggestions && (
        <div style={{ marginTop: "30px" }}>
          <h2>💡 Suggestions</h2>
          <div style={{
            backgroundColor: "#fff6e5",
            padding: "20px",
            borderRadius: "10px",
            border: "1px solid #f0c36d",
            fontFamily: "Segoe UI, sans-serif",
            lineHeight: "1.6"
          }}>
            {suggestions.split("\n").map((line, index) => (
              <div key={index}>
                {line.startsWith("**") ? (
                  <h3 style={{ marginTop: "20px", color: "#cc7000" }}>
                    {line.replace(/\*\*/g, "")}
                  </h3>
                ) : (
                  <p style={{ margin: "4px 0" }}>{line}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
