// Configuration
const API_BASE_URL = 'http://localhost:8080';

// Global state variables
let matchChartInstance = null;

// Page Initialization Route
document.addEventListener('DOMContentLoaded', () => {
    const isLoginPage = document.getElementById('loginForm') !== null || document.getElementById('registerForm') !== null;
    const isDashboardPage = document.getElementById('uploadForm') !== null;

    if (isLoginPage) {
        initLoginPage();
    } else if (isDashboardPage) {
        initDashboardPage();
    }
});

// ==========================================
// AUTHENTICATION & LOGIN PAGE LOGIC
// ==========================================

function initLoginPage() {
    const token = localStorage.getItem('skillgraph_token');
    if (token) {
        // Already logged in, redirect
        window.location.href = 'dashboard.html';
        return;
    }

    const loginSection = document.getElementById('loginSection');
    const registerSection = document.getElementById('registerSection');
    const toRegister = document.getElementById('toRegister');
    const toLogin = document.getElementById('toLogin');
    
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const authAlert = document.getElementById('authAlert');

    // Toggle views
    toRegister.addEventListener('click', (e) => {
        e.preventDefault();
        hideAlert(authAlert);
        loginSection.classList.add('d-none');
        registerSection.classList.remove('d-none');
    });

    toLogin.addEventListener('click', (e) => {
        e.preventDefault();
        hideAlert(authAlert);
        registerSection.classList.add('d-none');
        loginSection.classList.remove('d-none');
    });

    // Handle Login Submit
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        const btnText = document.getElementById('loginBtnText');
        const spinner = document.getElementById('loginSpinner');
        
        setLoading(true, btnText, spinner);
        hideAlert(authAlert);

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Login failed. Please check credentials.');
            }

            // Save credentials
            localStorage.setItem('skillgraph_token', data.token);
            localStorage.setItem('skillgraph_username', data.fullName);
            localStorage.setItem('skillgraph_email', data.email);

            showAlert(authAlert, 'success', 'Login successful! Redirecting...');
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);

        } catch (err) {
            showAlert(authAlert, 'danger', err.message);
            setLoading(false, btnText, spinner);
        }
    });

    // Handle Register Submit
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fullName = document.getElementById('regName').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        const careerGoal = document.getElementById('regGoal').value;

        const btnText = document.getElementById('registerBtnText');
        const spinner = document.getElementById('registerSpinner');

        setLoading(true, btnText, spinner);
        hideAlert(authAlert);

        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ fullName, email, password, careerGoal })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Registration failed.');
            }

            showAlert(authAlert, 'success', 'Registration successful! You can now log in.');
            registerForm.reset();
            
            // Switch back to login page
            setTimeout(() => {
                toLogin.click();
                document.getElementById('loginEmail').value = email;
            }, 1500);

        } catch (err) {
            showAlert(authAlert, 'danger', err.message);
            setLoading(false, btnText, spinner);
        }
    });
}

// ==========================================
// DASHBOARD PAGE LOGIC
// ==========================================

function initDashboardPage() {
    const token = localStorage.getItem('skillgraph_token');
    if (!token) {
        // Not authenticated, redirect to login
        window.location.href = 'login.html';
        return;
    }

    // Set user headers
    const userName = localStorage.getItem('skillgraph_username') || 'Developer';
    document.getElementById('navUserName').innerText = userName;
    document.getElementById('welcomeName').innerText = userName;

    // Load initial profile & analysis
    loadUserProfile();
    loadLatestAnalysis();

    // Setup Logout
    document.getElementById('logoutBtn').addEventListener('click', logout);

    // Setup Dropzone & File handlers
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resumeFileInput');
    const selectedFileName = document.getElementById('selectedFileName');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const uploadForm = document.getElementById('uploadForm');
    const dashboardAlert = document.getElementById('dashboardAlert');

    // Click to select
    dropZone.addEventListener('click', () => fileInput.click());

    // File input changes
    fileInput.addEventListener('change', (e) => {
        handleFileSelection(e.target.files[0]);
    });

    // Drag-and-drop actions
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.style.borderColor = 'var(--primary)';
            dropZone.style.background = 'rgba(99, 102, 241, 0.1)';
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            dropZone.style.background = 'rgba(15, 23, 42, 0.2)';
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        if (file) {
            fileInput.files = dt.files;
            handleFileSelection(file);
        }
    });

    function handleFileSelection(file) {
        if (!file) return;
        
        const ext = file.name.split('.').pop().toLowerCase();
        if (ext !== 'pdf' && ext !== 'docx') {
            showAlert(dashboardAlert, 'danger', 'Invalid file type. Please upload a PDF or DOCX file.');
            fileInput.value = '';
            selectedFileName.innerText = 'No file selected';
            analyzeBtn.disabled = true;
            return;
        }

        selectedFileName.innerText = `${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
        analyzeBtn.disabled = false;
        hideAlert(dashboardAlert);
    }

    // Handle Upload & Analysis Submit
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const file = fileInput.files[0];
        if (!file) return;

        const spinner = document.getElementById('analyzeSpinner');
        const btnSpan = analyzeBtn.querySelector('span');

        setLoading(true, btnSpan, spinner);
        analyzeBtn.disabled = true;
        hideAlert(dashboardAlert);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/api/resume/upload`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Parsing failed.');
            }

            showAlert(dashboardAlert, 'success', 'Resume parsed and analyzed successfully!');
            renderAnalysisResults(data);
            
            // Reset upload form
            uploadForm.reset();
            selectedFileName.innerText = 'No file selected';

        } catch (err) {
            showAlert(dashboardAlert, 'danger', err.message);
        } finally {
            setLoading(false, btnSpan, spinner);
        }
    });

    // Update Career Goal
    const goalSelect = document.getElementById('profileGoalSelect');
    const updateGoalBtn = document.getElementById('updateGoalBtn');

    updateGoalBtn.addEventListener('click', async () => {
        const targetGoal = goalSelect.value;
        updateGoalBtn.disabled = true;
        hideAlert(dashboardAlert);

        try {
            const response = await fetch(`${API_BASE_URL}/api/user/profile`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ careerGoal: targetGoal })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to update goal');
            }

            // Success
            localStorage.setItem('skillgraph_goal', data.careerGoal);
            document.getElementById('navCareerGoal').innerText = data.careerGoal;
            showAlert(dashboardAlert, 'success', `Career goal updated to ${data.careerGoal}. Please re-upload your resume to perform gap analysis.`);
            
            // Hide previous results as they are outdated
            document.getElementById('resultsDashboard').classList.add('d-none');

        } catch (err) {
            showAlert(dashboardAlert, 'danger', err.message);
        } finally {
            updateGoalBtn.disabled = false;
        }
    });

    // PDF Report Generator Download Action
    const pdfReportBtn = document.getElementById('pdfReportBtn');
    pdfReportBtn.addEventListener('click', async () => {
        const spinner = document.getElementById('pdfSpinner');
        pdfReportBtn.disabled = true;
        spinner.classList.remove('d-none');

        try {
            const response = await fetch(`${API_BASE_URL}/api/resume/report`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to generate PDF report.');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `SkillGraph_AI_Report_${localStorage.getItem('skillgraph_username').replace(/\s+/g, '_')}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);

        } catch (err) {
            showAlert(dashboardAlert, 'danger', err.message);
        } finally {
            pdfReportBtn.disabled = false;
            spinner.classList.add('d-none');
        }
    });
}

// Load profile info
async function loadUserProfile() {
    const token = localStorage.getItem('skillgraph_token');
    try {
        const response = await fetch(`${API_BASE_URL}/api/user/profile`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('skillgraph_goal', data.careerGoal);
            document.getElementById('navCareerGoal').innerText = data.careerGoal;
            document.getElementById('profileGoalSelect').value = data.careerGoal;
        }
    } catch (e) {
        console.error("Failed to load user profile", e);
    }
}

// Load latest analysis
async function loadLatestAnalysis() {
    const token = localStorage.getItem('skillgraph_token');
    try {
        const response = await fetch(`${API_BASE_URL}/api/resume/analysis`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (response.status === 404) {
            // No analysis yet, do nothing
            return;
        }

        const data = await response.json();
        if (response.ok) {
            renderAnalysisResults(data);
        }
    } catch (e) {
        console.error("Failed to load analysis", e);
    }
}

// Renders all components of the analysis data onto the DOM
function renderAnalysisResults(data) {
    const resultsDiv = document.getElementById('resultsDashboard');
    resultsDiv.classList.remove('d-none');
    
    // Smooth scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });

    // 1. Render charts
    renderDoughnutChart(data.matchPercentage);

    // 2. Skill lists
    const matchedList = document.getElementById('matchedSkillsList');
    const missingList = document.getElementById('missingSkillsList');
    
    document.getElementById('matchedCount').innerText = data.extractedSkills.length;
    document.getElementById('missingCount').innerText = data.missingSkills.length;

    matchedList.innerHTML = '';
    data.extractedSkills.forEach(skill => {
        const badge = document.createElement('span');
        badge.className = 'skills-badge matched animate__animated animate__fadeIn';
        badge.innerHTML = `<i class="bi bi-check-lg me-1"></i>${skill}`;
        matchedList.appendChild(badge);
    });

    missingList.innerHTML = '';
    if (data.missingSkills.length === 0) {
        missingList.innerHTML = '<span class="text-secondary small">No missing skills! You match 100% of target criteria.</span>';
    } else {
        data.missingSkills.forEach(skill => {
            const badge = document.createElement('span');
            badge.className = 'skills-badge missing animate__animated animate__fadeIn';
            badge.innerHTML = `<i class="bi bi-x-lg me-1"></i>${skill}`;
            missingList.appendChild(badge);
        });
    }

    // 3. Roadmap Timeline
    const timeline = document.getElementById('timelineContainer');
    timeline.innerHTML = '';
    
    if (data.learningRoadmap.length === 0) {
        timeline.innerHTML = '<p class="text-secondary small mb-0">No roadmap necessary. You are fully qualified!</p>';
    } else {
        data.learningRoadmap.forEach(item => {
            const timeItem = document.createElement('div');
            timeItem.className = 'timeline-item';
            timeItem.innerHTML = `
                <div class="timeline-badge"></div>
                <div class="timeline-content">
                    <div class="timeline-step">${item.milestone}</div>
                    <div class="timeline-title">${item.skill}</div>
                    <p class="timeline-desc">${item.description}</p>
                </div>
            `;
            timeline.appendChild(timeItem);
        });
    }

    // 4. Certifications recommendations
    const certsGrid = document.getElementById('certsGrid');
    certsGrid.innerHTML = '';
    
    if (data.certifications.length === 0) {
        certsGrid.innerHTML = '<div class="col-12"><p class="text-secondary small mb-0">No certification recommendations needed.</p></div>';
    } else {
        data.certifications.forEach(cert => {
            const cardDiv = document.createElement('div');
            cardDiv.className = 'col-sm-6 col-lg-12 col-xl-6';
            cardDiv.innerHTML = `
                <div class="cert-card">
                    <i class="bi bi-award cert-icon"></i>
                    <h6 class="text-white fw-bold mb-1">${cert.certification}</h6>
                    <p class="small text-secondary mb-0">Validates: <b>${cert.skill}</b></p>
                </div>
            `;
            certsGrid.appendChild(cardDiv);
        });
    }
}

// Renders the circular doughnut chart using Chart.js
function renderDoughnutChart(percentage) {
    const ctx = document.getElementById('matchScoreChart').getContext('2d');
    
    // Update match score text
    document.getElementById('matchScoreText').innerText = `${percentage}%`;

    // Destroy existing instance to avoid canvas re-render hover errors
    if (matchChartInstance !== null) {
        matchChartInstance.destroy();
    }

    matchChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Match', 'Gap'],
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [
                    '#06b6d4', // Cyan accent
                    'rgba(255, 255, 255, 0.05)' // Semi transparent gap
                ],
                borderWidth: 0,
                hoverOffset: 0
            }]
        },
        options: {
            cutout: '80%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

function showAlert(element, type, message) {
    element.className = `alert alert-${type} animated-fade-in`;
    element.innerText = message;
    element.classList.remove('d-none');
}

function hideAlert(element) {
    element.classList.add('d-none');
}

function setLoading(isLoading, textElement, spinnerElement) {
    if (isLoading) {
        if (textElement) textElement.classList.add('d-none');
        if (spinnerElement) spinnerElement.classList.remove('d-none');
    } else {
        if (textElement) textElement.classList.remove('d-none');
        if (spinnerElement) spinnerElement.classList.add('d-none');
    }
}

async function logout() {
    const token = localStorage.getItem('skillgraph_token');
    
    // Attempt backend logout (cleanup)
    try {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
    } catch (e) {
        console.error("Sign-out warning:", e);
    }

    // Clear local storage
    localStorage.removeItem('skillgraph_token');
    localStorage.removeItem('skillgraph_username');
    localStorage.removeItem('skillgraph_email');
    localStorage.removeItem('skillgraph_goal');

    window.location.href = 'login.html';
}
