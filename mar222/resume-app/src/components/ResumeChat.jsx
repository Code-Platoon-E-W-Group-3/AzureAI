import { useState } from 'react';

function ResumeChat({ resumeData }) {
    const [question, setQuestion] = useState('');
    const [response, setResponse] = useState('');

    const handleChat = async () => {
        if (!question) return;
    
        try {
            const res = await fetch('http://localhost:8000/api/chat-resume/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_data: resumeData, question }),
            });
    
            const data = await res.json();
            setResponse(data.response || 'No response received.');
        } catch (error) {
            console.error('Chat error:', error);
        }
    };
    
    };

    return (
        <div>
            <h3>Chat About Your Resume</h3>
            <input type="text" placeholder="Ask about your resume..." value={question} onChange={(e) => setQuestion(e.target.value)} />
            <button onClick={handleChat}>Send</button>
            {response && <p><strong>AI Response:</strong> {response}</p>}
        </div>
    );
}

export default ResumeChat;
