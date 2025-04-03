import { useState } from 'react';

function ResumeUploader() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileUpload = (event) => {
        const file = event.target.files[0]
        console.log(file)
        setSelectedFile(file);
    };

    const handleAnalyze = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('resume', selectedFile);

        try {
            const response = await fetch('http://localhost:8000/api/resume-analyze/', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Error analyzing resume:', error);
        }
    };

    return (
        <div>
            <h2>Upload Your Resume</h2>
            <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileUpload} />
            <button onClick={handleAnalyze}>Analyze Resume</button>
            {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
        </div>
    );
}

export default ResumeUploader;
