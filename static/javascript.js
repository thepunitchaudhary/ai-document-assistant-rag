// Display the selected file name in the UI
document.getElementById('pdfFile').addEventListener('change', function() {
    const fileNameDisplay = document.getElementById('fileName');
    fileNameDisplay.textContent = this.files[0] ? this.files[0].name : "No file selected";
});

// Handle 'Enter' key press
function handleEnter(event) {
    if (event.key === 'Enter') {
        sendQuery();
    }
}

async function uploadDoc() {
    const fileInput = document.getElementById('pdfFile');
    const statusMsg = document.getElementById('uploadStatus');
    
    if (!fileInput.files[0]) {
        statusMsg.style.color = "#ff4a4a";
        statusMsg.textContent = "Please select a file first.";
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    statusMsg.style.color = "#10a37f";
    statusMsg.textContent = "Processing document...";
    
    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        const result = await response.json();
        
        if(response.ok) {
            statusMsg.textContent = "✅ " + result.message;
        } else {
            statusMsg.style.color = "#ff4a4a";
            statusMsg.textContent = "Error processing document.";
        }
    } catch (error) {
        statusMsg.style.color = "#ff4a4a";
        statusMsg.textContent = "Network error.";
    }
}

async function sendQuery() {
    const queryInput = document.getElementById('userQuery');
    const chatBox = document.getElementById('chatBox');
    const query = queryInput.value.trim();
    
    if (!query) return;

    // 1. Add User Message to UI
    chatBox.innerHTML += `
        <div class="message user-message">
            <div class="avatar user-avatar">U</div>
            <div class="message-content">${query}</div>
        </div>
    `;
    
    // Clear input and scroll to bottom
    queryInput.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // 2. Add temporary "Thinking..." message
    const thinkingId = "thinking-" + Date.now();
    chatBox.innerHTML += `
        <div class="message ai-message" id="${thinkingId}">
            <div class="avatar ai-avatar">AI</div>
            <div class="message-content" style="color: #9ca3af;">Thinking...</div>
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    // 3. Send to Backend
    const formData = new FormData();
    formData.append('query', query);

    try {
        const response = await fetch('/ask', { method: 'POST', body: formData });
        const result = await response.json();
        
        // 4. Remove "Thinking" message and add actual response
        document.getElementById(thinkingId).remove();
        
        chatBox.innerHTML += `
            <div class="message ai-message">
                <div class="avatar ai-avatar">AI</div>
                <div class="message-content">${result.answer}</div>
            </div>
        `;
    } catch (error) {
        document.getElementById(thinkingId).remove();
        chatBox.innerHTML += `
            <div class="message ai-message">
                <div class="avatar ai-avatar">AI</div>
                <div class="message-content" style="color: #ff4a4a;">Sorry, I encountered an error. Make sure you uploaded a document first!</div>
            </div>
        `;
    }
    
    chatBox.scrollTop = chatBox.scrollHeight;
}