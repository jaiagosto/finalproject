// API Configuration
const API_BASE = window.location.origin;

// State management
let currentUser = null;
let token = localStorage.getItem('token');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        loadUserData();
    } else {
        showAuthSection();
    }
    
    setupEventListeners();
});

// Event listeners
function setupEventListeners() {
    // Auth forms
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
    document.getElementById('registerForm')?.addEventListener('submit', handleRegister);
    document.getElementById('logoutBtn')?.addEventListener('click', handleLogout);
    
    // Calculator form
    document.getElementById('calculatorForm')?.addEventListener('submit', handleCalculation);
    
    // Profile forms
    document.getElementById('profileForm')?.addEventListener('submit', handleProfileUpdate);
    document.getElementById('passwordForm')?.addEventListener('submit', handlePasswordChange);
    
    // Navigation
    document.querySelectorAll('[data-nav]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const section = e.target.dataset.nav;
            showSection(section);
        });
    });
    
    // Clear history
    document.getElementById('clearHistoryBtn')?.addEventListener('click', handleClearHistory);
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            token = data.access_token;
            localStorage.setItem('token', token);
            showAlert('Login successful!', 'success');
            loadUserData();
        } else {
            showAlert(data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const userData = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password')
    };
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Registration successful! Please login.', 'success');
            document.getElementById('registerForm').reset();
            showSection('login');
        } else {
            showAlert(data.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

async function handleLogout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    token = null;
    currentUser = null;
    localStorage.removeItem('token');
    showAuthSection();
    showAlert('Logged out successfully', 'success');
}

async function loadUserData() {
    try {
        const response = await fetch(`${API_BASE}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            showAppSection();
            loadDashboard();
        } else {
            handleLogout();
        }
    } catch (error) {
        showAlert('Failed to load user data', 'error');
        handleLogout();
    }
}

// Calculator operations
async function handleCalculation(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const calcData = {
        operation: formData.get('operation'),
        operand1: parseFloat(formData.get('operand1')),
        operand2: parseFloat(formData.get('operand2'))
    };
    
    try {
        const response = await fetch(`${API_BASE}/calculations/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(calcData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('calcResult').textContent = data.result;
            document.getElementById('resultDisplay').classList.remove('hidden');
            showAlert('Calculation completed!', 'success');
            
            // Refresh history if on history page
            if (!document.getElementById('historySection').classList.contains('hidden')) {
                loadHistory();
            }
        } else {
            showAlert(data.detail || 'Calculation failed', 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/analytics/summary`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            displayAnalytics(data);
        }
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

function displayAnalytics(data) {
    document.getElementById('totalCalcs').textContent = data.total_calculations;
    document.getElementById('mostUsed').textContent = data.most_used_operation || 'N/A';
    document.getElementById('avgResult').textContent = 
        data.average_result ? data.average_result.toFixed(2) : 'N/A';
    
    // Display operations breakdown
    const breakdownHtml = data.operations_breakdown.map(op => `
        <div class="operation-stat">
            <span class="badge badge-${op.operation}">${op.operation}</span>
            <span>${op.count} (${op.percentage}%)</span>
        </div>
    `).join('');
    
    document.getElementById('operationsBreakdown').innerHTML = breakdownHtml || '<p>No calculations yet</p>';
}

// History
async function loadHistory(page = 0) {
    const limit = 10;
    const offset = page * limit;
    
    try {
        const response = await fetch(
            `${API_BASE}/analytics/history?limit=${limit}&offset=${offset}`,
            {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            }
        );
        
        if (response.ok) {
            const data = await response.json();
            displayHistory(data.items);
            setupPagination(data, page);
        }
    } catch (error) {
        showAlert('Failed to load history', 'error');
    }
}

function displayHistory(calculations) {
    const tbody = document.getElementById('historyTableBody');
    
    if (calculations.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No calculations found</td></tr>';
        return;
    }
    
    const html = calculations.map(calc => `
        <tr>
            <td><span class="badge badge-${calc.operation}">${calc.operation}</span></td>
            <td>${calc.operand1}</td>
            <td>${calc.operand2}</td>
            <td><strong>${calc.result}</strong></td>
            <td>${new Date(calc.created_at).toLocaleString()}</td>
        </tr>
    `).join('');
    
    tbody.innerHTML = html;
}

function setupPagination(data, currentPage) {
    const totalPages = Math.ceil(data.total / data.limit);
    const paginationHtml = `
        <button ${currentPage === 0 ? 'disabled' : ''} onclick="loadHistory(${currentPage - 1})">
            Previous
        </button>
        <span>Page ${currentPage + 1} of ${totalPages}</span>
        <button ${!data.has_more ? 'disabled' : ''} onclick="loadHistory(${currentPage + 1})">
            Next
        </button>
    `;
    
    document.getElementById('pagination').innerHTML = paginationHtml;
}

async function handleClearHistory() {
    if (!confirm('Are you sure you want to clear all calculation history?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/analytics/history`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('History cleared successfully', 'success');
            loadHistory();
            loadDashboard();
        }
    } catch (error) {
        showAlert('Failed to clear history', 'error');
    }
}

// Profile management
async function handleProfileUpdate(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const profileData = {
        username: formData.get('username'),
        email: formData.get('email')
    };
    
    try {
        const response = await fetch(`${API_BASE}/users/profile`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(profileData)
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser = data;
            showAlert('Profile updated successfully', 'success');
            document.getElementById('userDisplay').textContent = currentUser.username;
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Update failed', 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

async function handlePasswordChange(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const passwordData = {
        current_password: formData.get('current_password'),
        new_password: formData.get('new_password')
    };
    
    try {
        const response = await fetch(`${API_BASE}/users/change-password`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(passwordData)
        });
        
        if (response.ok) {
            showAlert('Password changed successfully', 'success');
            document.getElementById('passwordForm').reset();
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Password change failed', 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

// UI helpers
function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.add('hidden');
    });
    
    document.getElementById(`${sectionName}Section`)?.classList.remove('hidden');
    
    // Load data when showing certain sections
    if (sectionName === 'dashboard') {
        loadDashboard();
    } else if (sectionName === 'history') {
        loadHistory();
    } else if (sectionName === 'profile') {
        loadProfileData();
    }
}

function showAuthSection() {
    document.getElementById('authContainer')?.classList.remove('hidden');
    document.getElementById('appContainer')?.classList.add('hidden');
    showSection('login');
}

function showAppSection() {
    document.getElementById('authContainer')?.classList.add('hidden');
    document.getElementById('appContainer')?.classList.remove('hidden');
    document.getElementById('userDisplay').textContent = currentUser.username;
    showSection('calculator');
}

function loadProfileData() {
    if (currentUser) {
        document.getElementById('profileUsername').value = currentUser.username;
        document.getElementById('profileEmail').value = currentUser.email;
    }
}

function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}