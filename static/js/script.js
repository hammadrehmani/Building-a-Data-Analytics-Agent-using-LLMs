// Initialize Markdown Parser
const md = window.markdownit({
    html: true,
    linkify: true,
    typographer: true
});

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const dropZoneContent = document.getElementById('dropZoneContent');
const fileInfoActive = document.getElementById('fileInfoActive');
const selectedFileName = document.getElementById('selectedFileName');
const selectedFileSize = document.getElementById('selectedFileSize');
const removeFileBtn = document.getElementById('removeFileBtn');
const questionTextarea = document.getElementById('question');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultSection = document.getElementById('resultSection');
const loadingContainer = document.getElementById('loading');
const resultContent = document.getElementById('resultContent');
const resultText = document.getElementById('resultText');
const chartContainer = document.getElementById('chartContainer');
const resultChart = document.getElementById('resultChart');
const loadingText = document.getElementById('loadingText');

let selectedFile = null;

// Drag and drop events
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    e.preventDefault();
    dropZone.classList.add('dragover');
}

function unhighlight(e) {
    e.preventDefault();
    dropZone.classList.remove('dragover');
}

dropZone.addEventListener('drop', handleDrop, false);
fileInput.addEventListener('change', handleFileSelect, false);
removeFileBtn.addEventListener('click', clearFile, false);
questionTextarea.addEventListener('input', validateForm);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    const validExtensions = ['.csv', '.xlsx'];
    const fileName = file.name;
    const fileExt = fileName.substring(fileName.lastIndexOf('.')).toLowerCase();
    
    if (!validExtensions.includes(fileExt)) {
        alert('Please upload a CSV or Excel (.xlsx) file only.');
        return;
    }

    selectedFile = file;
    selectedFileName.textContent = file.name;
    
    // Format file size
    const sizeInKB = (file.size / 1024).toFixed(1);
    if (sizeInKB > 1024) {
        selectedFileSize.textContent = `${(sizeInKB / 1024).toFixed(1)} MB`;
    } else {
        selectedFileSize.textContent = `${sizeInKB} KB`;
    }

    // Toggle views
    dropZoneContent.style.display = 'none';
    fileInfoActive.style.display = 'flex';
    validateForm();
}

function clearFile(e) {
    if (e) e.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    dropZoneContent.style.display = 'flex';
    fileInfoActive.style.display = 'none';
    validateForm();
}

function validateForm() {
    const question = questionTextarea.value.trim();
    if (selectedFile && question.length > 0) {
        analyzeBtn.removeAttribute('disabled');
    } else {
        analyzeBtn.setAttribute('disabled', 'true');
    }
}

// Loading message rotator
const loadingMessages = [
    "Uploading dataset...",
    "Reading file structure...",
    "Understanding headers and data types...",
    "Sending query to AI Agent...",
    "Generating Python code...",
    "Executing analysis code...",
    "Formulating response...",
    "Almost there..."
];

let messageInterval = null;

function startLoadingAnimation() {
    let index = 0;
    loadingText.textContent = loadingMessages[0];
    messageInterval = setInterval(() => {
        index = (index + 1) % loadingMessages.length;
        loadingText.textContent = loadingMessages[index];
    }, 4000);
}

function stopLoadingAnimation() {
    if (messageInterval) {
        clearInterval(messageInterval);
        messageInterval = null;
    }
}

async function analyzeData() {
    if (!selectedFile) return;
    const question = questionTextarea.value.trim();
    if (!question) return;

    // Show result section and loading state
    resultSection.style.display = 'block';
    loadingContainer.style.display = 'flex';
    resultContent.style.display = 'none';
    chartContainer.style.display = 'none';
    
    // Disable inputs during analysis
    analyzeBtn.setAttribute('disabled', 'true');
    questionTextarea.setAttribute('disabled', 'true');
    fileInput.setAttribute('disabled', 'true');
    removeFileBtn.style.display = 'none';

    startLoadingAnimation();

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("query", question);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        // Render Markdown answer
        resultText.innerHTML = md.render(data.answer || "No answer returned by agent.");
        
        // Show chart if generated
        if (data.has_chart && data.chart_url) {
            // Append a timestamp parameter to force browser image cache refresh
            resultChart.src = `${data.chart_url}?t=${new Date().getTime()}`;
            chartContainer.style.display = 'block';
        } else {
            chartContainer.style.display = 'none';
        }

        // Show contents
        resultContent.style.display = 'block';
    } catch (error) {
        console.error("Analysis Error:", error);
        resultText.innerHTML = `<div style="color: #ef4444; font-weight: 500;"><i class="fa-solid fa-triangle-exclamation"></i> Error occurred during analysis: ${error.message}</div>`;
        resultContent.style.display = 'block';
    } finally {
        stopLoadingAnimation();
        loadingContainer.style.display = 'none';
        
        // Re-enable inputs
        analyzeBtn.removeAttribute('disabled');
        questionTextarea.removeAttribute('disabled');
        fileInput.removeAttribute('disabled');
        removeFileBtn.style.display = 'flex';
        
        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
}