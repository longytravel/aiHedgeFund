import React from 'react'
import ReactDOM from 'react-dom/client'

const App = () => {
  return (
    <div style={{ padding: '2rem', fontFamily: 'system-ui' }}>
      <h1>AIHedgeFund</h1>
      <p>AI-powered UK stock analysis platform</p>
      <p>Dashboard coming soon...</p>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
