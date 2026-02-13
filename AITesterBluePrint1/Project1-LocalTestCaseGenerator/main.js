import { executeTestGeneration } from './src/logic/navigator.js';
import { checkOllamaStatus } from './src/api/ollama.js';

window.onerror = function (msg, url, lineNo, columnNo, error) {
    console.error('PILOT ERROR:', msg, '\nURL:', url, '\nLine:', lineNo, '\nCol:', columnNo, '\nError:', error);
    return false;
};

const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const statusBadge = document.getElementById('ollama-status');

// Update status badge
async function updateStatus() {
    console.log('Checking Pilot Backend status...');
    const isOnline = await checkOllamaStatus();
    console.log('Backend Online:', isOnline);

    if (!statusBadge) {
        console.error('Status badge element not found');
        return;
    }

    if (isOnline) {
        statusBadge.textContent = 'Pilot: Online';
        statusBadge.style.color = '#3fb950';
        statusBadge.classList.add('online');
    } else {
        statusBadge.textContent = 'Pilot: Offline (Check Backend)';
        statusBadge.style.color = '#f85149';
        statusBadge.classList.remove('online');
    }
}

function appendMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    msgDiv.textContent = content;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msgDiv;
}

// Simple Markdown-ish display for code blocks
function formatContent(content) {
    if (typeof marked !== 'undefined') {
        return marked.parse(content);
    }
    return content.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
}

async function handleSend() {
    const code = userInput.value.trim();
    if (!code) return;

    userInput.value = '';
    appendMessage('user', code);

    const assistantMsg = appendMessage('assistant', 'Routing to Pilot SOP...');

    try {
        await executeTestGeneration(code, (fullOutput) => {
            assistantMsg.innerHTML = formatContent(fullOutput);
            // Trigger Prism highlighting for new code blocks
            if (typeof Prism !== 'undefined') {
                Prism.highlightAllUnder(assistantMsg);
            }
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    } catch (error) {
        assistantMsg.textContent = 'Pilot Error: ' + error.message;
    }
}

sendBtn.addEventListener('click', handleSend);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

updateStatus();
setInterval(updateStatus, 5000);
