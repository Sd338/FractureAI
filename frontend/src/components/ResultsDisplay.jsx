import React from 'react';
import './resultsdisplay.css';

const ResultsDisplay = ({ results }) => {
    if (!results) {
        return <div className="error-message">No results to display.</div>;
    }

    return (
        <div className="results-container">
            <div className="results-header">
                <h2>Analysis Results</h2>
            </div>
            {results.map((result, index) => (
                <div className="result-card" key={index}>
                    <div className="result-info">
                        <p>{result.description}</p>
                        <p>Confidence: {result.confidence}%</p>
                    </div>
                </div>
            ))}
            <a href="http://your-hugging-face-space-url" className="cta-button">
                Analyze Another X-ray
            </a>
            <footer>
                <p>&copy; 2024 FractureAI. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default ResultsDisplay;
