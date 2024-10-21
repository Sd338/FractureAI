import React, { useState } from 'react';
import './upload.css'; // Create a separate CSS file for styles

const Upload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setError(''); // Clear any previous errors
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select an image to upload.');
            return;
        }

        setLoading(true);
        // Simulate an API call for file upload
        setTimeout(() => {
            setLoading(false);
            alert('File uploaded successfully!'); // Replace with actual API call response handling
            setFile(null); // Reset the file input
        }, 2000);
    };

    return (
        <div className="upload-container">
            <h2>Upload Your X-ray Image</h2>
            <div className="upload-area">
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="upload-input"
                />
                <button
                    onClick={handleUpload}
                    className="cta-button"
                    disabled={loading}
                >
                    {loading ? 'Uploading...' : 'Upload Image'}
                </button>
                {error && <p className="error-message">{error}</p>}
            </div>
        </div>
    );
};

export default Upload;
