document.addEventListener('DOMContentLoaded', () => {
    const translateBtn = document.getElementById('translateBtn');
    
    translateBtn.addEventListener('click', async () => {
        const text = document.getElementById('text').value;
        const inputLang = document.getElementById('input_lang').value;
        const outputLang = document.getElementById('output_lang').value;
        const tone = document.getElementById('tone').value;
        const output = document.getElementById('output');
        
        if (!text) {
            output.textContent = 'Please enter text';
            return;
        }

        output.textContent = 'Translating...';
        
        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    input_language: inputLang,
                    output_language: outputLang,
                    tone: tone
                })
            });

            // First check if the response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Then try to parse the JSON
            const data = await response.json();
            
            if (data && data.translation) {
                output.textContent = data.translation;
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            output.textContent = 'Error: ' + error.message;
            console.error('Translation error:', error);
            console.error('Full error object:', error);
        }
    });
});