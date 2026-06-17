const BASE_URL = 'http://localhost:8001/api/v1';
const USER_ID = 'fcc742fa-a6ca-48c7-944c-7989287ede9f';

// State holding all loaded items
let appData = {
    tasks: [],
    ideas: [],
    notes: [],
    shopitems: []
};

// Available priority levels strictly defined by Eisenhower matrix
const PRIORITY_LEVELS = [
    'Important & Urgent',
    'Important & Not Urgent',
    'Not Important & Urgent',
    'Not Important & Not Urgent'
];

document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
});

// ==========================================
// Tabs Logic
// ==========================================

function switchTab(tabId) {
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.add('hidden');
        panel.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const targetPanel = document.getElementById(tabId);
    if (targetPanel) {
        targetPanel.classList.remove('hidden');
        targetPanel.classList.add('active');
    }
    
    const targetBtn = document.getElementById(`btn-${tabId}`);
    if (targetBtn) {
        targetBtn.classList.add('active');
    }
}

// ==========================================
// API Calls
// ==========================================

async function fetchDashboardData() {
    try {
        const response = await fetch(`${BASE_URL}/dashboard/${USER_ID}`);
        if (!response.ok) throw new Error('Failed to fetch dashboard data');
        const data = await response.json();
        appData = data;
        renderAll();
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Could not connect to the server. Please make sure the backend is running.');
    }
}

async function apiRequest(endpoint, method, payload = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (payload) options.body = JSON.stringify(payload);

    const response = await fetch(`${BASE_URL}${endpoint}`, options);
    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || 'API Error');
    }
    return method !== 'DELETE' ? await response.json() : await response.json();
}

// ==========================================
// Rendering Logic
// ==========================================

function renderAll() {
    renderTasks();
    renderList('ideas', appData.ideas, 'ideas-list', 'title', 'description');
    renderList('notes', appData.notes, 'notes-list', 'content', 'summary');
    renderList('shopitems', appData.shopitems, 'shoplist', 'item_name', 'description');
}

function renderTasks() {
    // Clear all quadrants
    document.getElementById('tasks-urgent-important').innerHTML = '';
    document.getElementById('tasks-not-urgent-important').innerHTML = '';
    document.getElementById('tasks-urgent-not-important').innerHTML = '';
    document.getElementById('tasks-not-urgent-not-important').innerHTML = '';

    appData.tasks.forEach(task => {
        const priority = task.priority || PRIORITY_LEVELS[2]; // Default if missing
        let containerId = 'tasks-urgent-not-important';

        switch (priority) {
            case PRIORITY_LEVELS[0]: containerId = 'tasks-urgent-important'; break;
            case PRIORITY_LEVELS[1]: containerId = 'tasks-not-urgent-important'; break;
            case PRIORITY_LEVELS[2]: containerId = 'tasks-urgent-not-important'; break;
            case PRIORITY_LEVELS[3]: containerId = 'tasks-not-urgent-not-important'; break;
        }

        const container = document.getElementById(containerId);
        if (container) {
            container.appendChild(createListItemHtml('tasks', task, task.title, task.description));
        }
    });
}

function renderList(entityType, items, containerId, titleField, subField) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    items.forEach(item => {
        container.appendChild(createListItemHtml(entityType, item, item[titleField], item[subField]));
    });
}

function createListItemHtml(entityType, item, titleStr, subStr) {
    const div = document.createElement('div');
    div.className = 'list-item';

    // Safely escape JS strings to avoid breakages in onclick
    const safeItem = encodeURIComponent(JSON.stringify(item));

    div.innerHTML = `
        <div class="item-content">
            <div class="item-bullet"></div>
            <div>
                <div class="item-text">${escapeHtml(titleStr || 'Untitled')}</div>
                ${subStr ? `<div class="item-subtext">${escapeHtml(subStr)}</div>` : ''}
            </div>
        </div>
        <div class="item-actions">
            <button class="icon-btn edit-btn" onclick="openModal('${entityType}', '${safeItem}')"><i class="fa-solid fa-pen"></i></button>
            <button class="icon-btn delete-btn" onclick="deleteItem('${entityType}', '${item.id}')"><i class="fa-solid fa-trash"></i></button>
        </div>
    `;
    return div;
}

// ==========================================
// Modal & Form Handling
// ==========================================

function openModal(entityType, encodedItem = null) {
    const modal = document.getElementById('unified-modal');
    const titleEl = document.getElementById('modal-title');
    const dynamicFields = document.getElementById('dynamic-fields');

    const isEdit = !!encodedItem;
    let item = null;
    if (isEdit) {
        item = JSON.parse(decodeURIComponent(encodedItem));
    }

    // Set hidden fields
    document.getElementById('entity-type').value = entityType;
    document.getElementById('entity-id').value = item ? item.id : '';

    titleEl.textContent = isEdit ? `Edit ${entityType.slice(0, -1)}` : `Add ${entityType.slice(0, -1)}`;
    dynamicFields.innerHTML = generateFormFields(entityType, item);

    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('unified-modal').classList.add('hidden');
    document.getElementById('unified-form').reset();
}

function generateFormFields(entityType, item) {
    let html = '';

    // Field definitions per entity
    const fields = {
        'tasks': [
            { id: 'title', label: 'Title', type: 'text', required: true, value: item?.title || '' },
            { id: 'description', label: 'Description', type: 'textarea', required: false, value: item?.description || '' },
            { id: 'priority', label: 'Priority', type: 'select', options: PRIORITY_LEVELS, required: true, value: item?.priority || PRIORITY_LEVELS[2] },
        ],
        'ideas': [
            { id: 'title', label: 'Idea Title', type: 'text', required: true, value: item?.title || '' },
            { id: 'description', label: 'Details', type: 'textarea', required: false, value: item?.description || '' }
        ],
        'notes': [
            { id: 'content', label: 'Content', type: 'textarea', required: true, value: item?.content || '' },
            { id: 'summary', label: 'Summary', type: 'text', required: false, value: item?.summary || '' }
        ],
        'shopitems': [
            { id: 'item_name', label: 'Item Name', type: 'text', required: true, value: item?.item_name || '' },
            { id: 'description', label: 'Description', type: 'text', required: false, value: item?.description || '' }
        ]
    };

    const entityFields = fields[entityType];

    entityFields.forEach(f => {
        html += `<div class="form-group">
            <label>${f.label}</label>`;

        if (f.type === 'textarea') {
            html += `<textarea id="form-${f.id}" class="form-control" name="${f.id}" rows="3" ${f.required ? 'required' : ''}>${f.value}</textarea>`;
        } else if (f.type === 'select') {
            html += `<select id="form-${f.id}" class="form-control" name="${f.id}" ${f.required ? 'required' : ''}>`;
            f.options.forEach(opt => {
                const selected = opt === f.value ? 'selected' : '';
                html += `<option value="${opt}" ${selected}>${opt}</option>`;
            });
            html += `</select>`;
        } else {
            html += `<input type="${f.type}" id="form-${f.id}" class="form-control" name="${f.id}" value="${f.value}" ${f.required ? 'required' : ''}>`;
        }

        html += `</div>`;
    });

    return html;
}

// ==========================================
// CRUD Actions
// ==========================================

async function handleFormSubmit(event) {
    event.preventDefault();
    const saveBtn = document.getElementById('modal-submit-btn');
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';

    const form = event.target;
    const entityType = document.getElementById('entity-type').value;
    const entityId = document.getElementById('entity-id').value;
    const isEdit = entityId !== '';

    // Collect all named inputs
    const payload = {};
    if (!isEdit) payload.user_id = USER_ID;

    // Use FormData to dynamically extract everything
    const formData = new FormData(form);
    for (let [key, value] of formData.entries()) {
        payload[key] = value;
    }

    try {
        if (isEdit) {
            await apiRequest(`/${entityType}/${entityId}`, 'PUT', payload);
        } else {
            await apiRequest(`/${entityType}`, 'POST', payload);
        }

        // Refresh local UI data instead of mutating strictly (easier state sync)
        await fetchDashboardData();
        closeModal();
    } catch (e) {
        console.error(e);
        alert('Failed to save item. Check console.');
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Save';
    }
}

async function deleteItem(entityType, id) {
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
        await apiRequest(`/${entityType}/${id}`, 'DELETE');
        await fetchDashboardData();
    } catch (e) {
        console.error(e);
        alert('Failed to delete item.');
    }
}

function escapeHtml(unsafe) {
    return (unsafe || '').toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// ==========================================
// Chatbot, Voice & AI Widget Logic
// ==========================================

function toggleAiMenu() {
    const mainWindow = document.getElementById('ai-main-window');
    mainWindow.classList.toggle('hidden');
    
    if (!mainWindow.classList.contains('hidden')) {
        setTimeout(() => document.getElementById('chat-input').focus(), 300);
    }
}

// Voice Recording Setup
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let currentStream;

async function toggleVoiceRecord() {
    const micBtn = document.getElementById('mic-action-btn');
    const inputField = document.getElementById('chat-input');
    
    if (!isRecording) {
        // Start recording
        try {
            currentStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(currentStream);
            audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                if (audioChunks.length > 0) {
                    await processAudioBlob(audioBlob);
                }
            };

            mediaRecorder.start();
            isRecording = true;
            
            // Update UI
            micBtn.style.color = "var(--accent-red)";
            micBtn.innerHTML = '<i class="fa-solid fa-stop"></i>'; // Change icon to stop
            inputField.placeholder = "Listening... (Tap stop to send)";
            inputField.disabled = true;
            
        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Could not access microphone. Please check permissions.");
        }
    } else {
        // Stop recording
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
        }
        if (currentStream) {
            currentStream.getTracks().forEach(track => track.stop());
            currentStream = null;
        }
        isRecording = false;
        
        // Reset UI
        micBtn.style.color = "";
        micBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
        inputField.placeholder = "Message ProdBuddy...";
        inputField.disabled = false;
        inputField.focus();
    }
}

async function processAudioBlob(blob) {
    // Convert Blob to Base64
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = async function() {
        // Gets "data:audio/webm;base64,....." -> we just want the base64 part
        const base64data = reader.result.split(',')[1];
        
        // Add optimistic UI message indicating transcription
        const userMsgId = addChatMessageToUI("🎙️ Transcribing audio...", 'user');

        try {
            const transcribePayload = {
                user_id: USER_ID,
                audio_base64: base64data
            };
            
            // 1. Send to Transcribe API
            const transcribeResponse = await apiRequest('/chat/transcribe/', 'POST', transcribePayload);
            
            let transcribedText = "🎙️ [Unintelligible Audio]";
            if (transcribeResponse && transcribeResponse.text) {
                transcribedText = transcribeResponse.text;
            }
            
            // Update the user's chat bubble with the actual text
            const userMsgEl = document.getElementById(userMsgId);
            if (userMsgEl) {
                userMsgEl.textContent = transcribedText;
            }
            
            // 2. Add 'thinking' state for the AI
            const thinkingId = addChatMessageToUI('ProdBuddy is thinking...', 'ai');
            
            // 3. Send the transcribed text to the normal Chat API
            const chatPayload = {
                user_id: USER_ID,
                message: transcribedText
            };
            
            const chatResponse = await apiRequest('/chat/', 'POST', chatPayload);
            
            // Update the AI's chat bubble
            const msgEl = document.getElementById(thinkingId);
            if (msgEl) {
                msgEl.textContent = chatResponse.reply || "Sorry, I didn't get a proper response.";
            } else {
                addChatMessageToUI(chatResponse.reply || "Error", 'ai');
            }

        } catch (error) {
            console.error('Error processing audio or chat:', error);
            const userMsgEl = document.getElementById(userMsgId);
            if (userMsgEl) userMsgEl.textContent += " (Failed to process)";
        }
    }
}

// Close AI widget if clicking outside of it
document.addEventListener('click', (event) => {
    const container = document.querySelector('.ai-widget-container');
    const mainWindow = document.getElementById('ai-main-window');
    
    if (container && mainWindow && !container.contains(event.target)) {
        mainWindow.classList.add('hidden');
    }
});

function handleChatEnter(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const inputEl = document.getElementById('chat-input');
    const messageText = inputEl.value.trim();
    if (!messageText) return;

    // Clear input
    inputEl.value = '';

    // Render User Message
    addChatMessageToUI(messageText, 'user');

    // Rendering thinking state (optional, just placeholder text)
    const thinkingId = addChatMessageToUI('ProdBuddy is thinking...', 'ai');

    try {
        const payload = {
            message: messageText,
            user_id: USER_ID
        };

        const response = await apiRequest('/chat/', 'POST', payload);

        // Update thinking state with actual response
        const msgEl = document.getElementById(thinkingId);
        if (msgEl) {
            msgEl.textContent = response.reply;
        } else {
             addChatMessageToUI(response.reply, 'ai');
        }

    } catch (error) {
        console.error('Chat Error:', error);
        const msgEl = document.getElementById(thinkingId);
        if (msgEl) {
            msgEl.textContent = 'Sorry, there was an error processing your request.';
        }
    }
}

function addChatMessageToUI(text, sender) {
    const container = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    // Ensure unique ID even if called multiple times in the same millisecond
    const msgId = 'msg-' + Date.now() + '-' + Math.floor(Math.random() * 10000);
    msgDiv.id = msgId;
    msgDiv.className = `chat-message ${sender}-message`;
    msgDiv.textContent = text;
    
    container.appendChild(msgDiv);
    
    // Auto scroll to bottom
    container.scrollTop = container.scrollHeight;
    
    return msgId;
}

