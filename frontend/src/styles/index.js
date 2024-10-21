import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Ensure this path is correct based on your file structure
import './styles/app.css'; // Global styles (if needed)
import reportWebVitals from './reportWebVitals'; // Optional for measuring performance

// Create a root element
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Optional: Measure performance
reportWebVitals();
