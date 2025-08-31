/**
 * AstraZeneca Clinical Trials - Main JavaScript File
 * Handles form validation, UI interactions, and dynamic content
 */

// Global variables
let bootstrapTooltips = [];
let bootstrapModals = [];

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeBootstrap();
    initializeFormValidation();
    initializeTableFeatures();
    initializeAccessibility();
    initializeAnimations();
});

/**
 * Initialize Bootstrap components
 */
function initializeBootstrap() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    bootstrapTooltips = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
}

/**
 * Form validation and enhancement
 */
function initializeFormValidation() {
    // Real-time validation for interest form
    const interestForm = document.querySelector('#interest-form, form[action*="interest"]');
    if (interestForm) {
        setupInterestFormValidation(interestForm);
    }

    // Admin search form enhancements
    const adminSearchForm = document.querySelector('form[method="GET"]');
    if (adminSearchForm) {
        setupAdminSearchForm(adminSearchForm);
    }
}

/**
 * Setup interest form validation
 */
function setupInterestFormValidation(form) {
    const nameInput = form.querySelector('#name');
    const emailInput = form.querySelector('#email');
    const mobileInput = form.querySelector('#mobile');
    const pincodeInput = form.querySelector('#pincode');
    const ageInput = form.querySelector('#age');
    const healthInfoInput = form.querySelector('#health_info');

    // Name validation
    if (nameInput) {
        nameInput.addEventListener('blur', function() {
            validateName(this);
        });
    }

    // Email validation
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateEmail(this);
        });
    }

    // Mobile number formatting and validation
    if (mobileInput) {
        mobileInput.addEventListener('input', function(e) {
            formatMobileNumber(e.target);
        });
        mobileInput.addEventListener('blur', function() {
            validateMobile(this);
        });
    }

    // Pincode formatting and validation
    if (pincodeInput) {
        pincodeInput.addEventListener('input', function(e) {
            formatPincode(e.target);
        });
        pincodeInput.addEventListener('blur', function() {
            validatePincode(this);
        });
    }

    // Age validation
    if (ageInput) {
        ageInput.addEventListener('blur', function() {
            validateAge(this);
        });
    }

    // Health info validation
    if (healthInfoInput) {
        const charCount = document.createElement('div');
        charCount.className = 'form-text text-end';
        charCount.id = 'health-info-count';
        healthInfoInput.parentNode.appendChild(charCount);

        healthInfoInput.addEventListener('input', function() {
            updateCharacterCount(this, charCount);
        });
        updateCharacterCount(healthInfoInput, charCount);
    }

    // Form submission validation
    form.addEventListener('submit', function(e) {
        if (!validateForm(form)) {
            e.preventDefault();
            showFormErrors();
        }
    });
}

/**
 * Validation functions
 */
function validateName(input) {
    const value = input.value.trim();
    const isValid = value.length >= 2 && value.length <= 100 && /^[a-zA-Z\s]+$/.test(value);
    
    setFieldValidation(input, isValid, isValid ? '' : 'Please enter a valid name (2-100 characters, letters only)');
    return isValid;
}

function validateEmail(input) {
    const value = input.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const isValid = emailRegex.test(value);
    
    setFieldValidation(input, isValid, isValid ? '' : 'Please enter a valid email address');
    return isValid;
}

function validateMobile(input) {
    const value = input.value.replace(/\D/g, '');
    const isValid = value.length === 10;
    
    setFieldValidation(input, isValid, isValid ? '' : 'Please enter a valid 10-digit mobile number');
    return isValid;
}

function validatePincode(input) {
    const value = input.value.replace(/\D/g, '');
    const isValid = value.length === 6;
    
    setFieldValidation(input, isValid, isValid ? '' : 'Please enter a valid 6-digit pincode');
    return isValid;
}

function validateAge(input) {
    const age = parseInt(input.value);
    const isValid = age >= 18 && age <= 120;
    
    let message = '';
    if (age < 18) {
        message = 'You must be at least 18 years old to participate';
    } else if (age > 120) {
        message = 'Please enter a valid age';
    }
    
    setFieldValidation(input, isValid, message);
    return isValid;
}

function setFieldValidation(input, isValid, message) {
    input.classList.remove('is-valid', 'is-invalid');
    
    // Remove existing feedback
    const existingFeedback = input.parentNode.querySelector('.invalid-feedback, .valid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    if (input.value.trim() !== '') {
        if (isValid) {
            input.classList.add('is-valid');
        } else {
            input.classList.add('is-invalid');
            if (message) {
                const feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                feedback.textContent = message;
                input.parentNode.appendChild(feedback);
            }
        }
    }
}

/**
 * Format mobile number input
 */
function formatMobileNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 10) {
        value = value.slice(0, 10);
    }
    input.value = value;
}

/**
 * Format pincode input
 */
function formatPincode(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 6) {
        value = value.slice(0, 6);
    }
    input.value = value;
}

/**
 * Update character count for textarea
 */
function updateCharacterCount(textarea, countElement) {
    const current = textarea.value.length;
    const max = 500;
    const remaining = max - current;
    
    countElement.textContent = `${current}/${max} characters`;
    
    if (remaining < 50) {
        countElement.className = 'form-text text-end text-warning';
    } else if (remaining < 20) {
        countElement.className = 'form-text text-end text-danger';
    } else {
        countElement.className = 'form-text text-end text-muted';
    }
}

/**
 * Validate entire form
 */
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(function(input) {
        const fieldValid = validateField(input);
        if (!fieldValid) {
            isValid = false;
        }
    });
    
    return isValid;
}

/**
 * Validate individual field based on type
 */
function validateField(input) {
    const type = input.type || input.tagName.toLowerCase();
    const id = input.id;
    
    switch (id) {
        case 'name':
            return validateName(input);
        case 'email':
            return validateEmail(input);
        case 'mobile':
            return validateMobile(input);
        case 'pincode':
            return validatePincode(input);
        case 'age':
            return validateAge(input);
        default:
            return input.value.trim() !== '';
    }
}

/**
 * Show form errors
 */
function showFormErrors() {
    const firstInvalidField = document.querySelector('.is-invalid');
    if (firstInvalidField) {
        firstInvalidField.focus();
        firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Show a general error message
    showNotification('Please correct the errors in the form and try again.', 'error');
}

/**
 * Setup admin search form
 */
function setupAdminSearchForm(form) {
    const pincodeInput = form.querySelector('#search_pincode');
    
    if (pincodeInput) {
        pincodeInput.addEventListener('input', function(e) {
            formatPincode(e.target);
        });
    }
    
    // Auto-submit on filter change
    const filterSelect = form.querySelector('#eligibility_filter');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            form.submit();
        });
    }
}

/**
 * Table features for admin dashboard
 */
function initializeTableFeatures() {
    // Sort table columns
    initializeTableSorting();
    
    // Export functionality
    initializeExportFeatures();
    
    // Row selection management
    initializeRowSelection();
}

/**
 * Initialize table sorting
 */
function initializeTableSorting() {
    const tables = document.querySelectorAll('table.sortable');
    
    tables.forEach(function(table) {
        const headers = table.querySelectorAll('th[data-sortable]');
        
        headers.forEach(function(header) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, header);
            });
        });
    });
}

/**
 * Sort table by column
 */
function sortTable(table, header) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const isAscending = header.classList.contains('sort-asc');
    
    // Remove existing sort classes
    header.parentNode.querySelectorAll('th').forEach(function(th) {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Add new sort class
    header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
    
    // Sort rows
    rows.sort(function(a, b) {
        const aValue = a.children[columnIndex].textContent.trim();
        const bValue = b.children[columnIndex].textContent.trim();
        
        const comparison = aValue.localeCompare(bValue, undefined, { numeric: true });
        return isAscending ? -comparison : comparison;
    });
    
    // Reorder rows
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

/**
 * Initialize export features
 */
function initializeExportFeatures() {
    const exportBtn = document.querySelector('#exportBtn');
    
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportTableToCSV();
        });
    }
}

/**
 * Export table to CSV
 */
function exportTableToCSV() {
    const table = document.querySelector('table');
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csvContent = [];
    
    rows.forEach(function(row) {
        const cells = row.querySelectorAll('th, td');
        const rowContent = [];
        
        cells.forEach(function(cell, index) {
            // Skip checkbox column
            if (index === 0 && cell.querySelector('input[type="checkbox"]')) {
                return;
            }
            
            const text = cell.textContent.trim().replace(/"/g, '""');
            rowContent.push(`"${text}"`);
        });
        
        if (rowContent.length > 0) {
            csvContent.push(rowContent.join(','));
        }
    });
    
    const csvString = csvContent.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `astrazeneca_submissions_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    
    window.URL.revokeObjectURL(url);
}

/**
 * Initialize row selection
 */
function initializeRowSelection() {
    const checkboxes = document.querySelectorAll('.submission-checkbox');
    
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            updateBulkActions();
        });
    });
}

/**
 * Update bulk action buttons
 */
function updateBulkActions() {
    const checkedBoxes = document.querySelectorAll('.submission-checkbox:checked');
    const bulkActionBtns = document.querySelectorAll('.bulk-action-btn');
    
    bulkActionBtns.forEach(function(btn) {
        btn.disabled = checkedBoxes.length === 0;
    });
    
    // Update counter
    const counter = document.querySelector('#selectedCount');
    if (counter) {
        counter.textContent = `${checkedBoxes.length} selected`;
    }
}

/**
 * Accessibility enhancements
 */
function initializeAccessibility() {
    // Add ARIA labels to interactive elements
    addAriaLabels();
    
    // Keyboard navigation
    setupKeyboardNavigation();
    
    // Focus management
    setupFocusManagement();
}

/**
 * Add ARIA labels
 */
function addAriaLabels() {
    // Add labels to buttons without text
    const iconButtons = document.querySelectorAll('button:not([aria-label]) i.fa');
    
    iconButtons.forEach(function(icon) {
        const button = icon.closest('button');
        if (button && !button.getAttribute('aria-label')) {
            const iconClass = icon.className;
            let label = 'Button';
            
            if (iconClass.includes('fa-eye')) label = 'View details';
            else if (iconClass.includes('fa-edit')) label = 'Edit';
            else if (iconClass.includes('fa-trash')) label = 'Delete';
            else if (iconClass.includes('fa-envelope')) label = 'Send email';
            
            button.setAttribute('aria-label', label);
        }
    });
}

/**
 * Setup keyboard navigation
 */
function setupKeyboardNavigation() {
    // Handle table navigation with arrow keys
    const tables = document.querySelectorAll('table');
    
    tables.forEach(function(table) {
        table.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT' && e.target.type === 'checkbox') {
                handleTableKeyNavigation(e, table);
            }
        });
    });
}

/**
 * Handle table keyboard navigation
 */
function handleTableKeyNavigation(e, table) {
    const currentCheckbox = e.target;
    const currentRow = currentCheckbox.closest('tr');
    const allCheckboxes = table.querySelectorAll('input[type="checkbox"]');
    const currentIndex = Array.from(allCheckboxes).indexOf(currentCheckbox);
    
    let targetIndex = currentIndex;
    
    switch (e.key) {
        case 'ArrowUp':
            e.preventDefault();
            targetIndex = Math.max(0, currentIndex - 1);
            break;
        case 'ArrowDown':
            e.preventDefault();
            targetIndex = Math.min(allCheckboxes.length - 1, currentIndex + 1);
            break;
        case 'Space':
            e.preventDefault();
            currentCheckbox.checked = !currentCheckbox.checked;
            currentCheckbox.dispatchEvent(new Event('change'));
            break;
    }
    
    if (targetIndex !== currentIndex && allCheckboxes[targetIndex]) {
        allCheckboxes[targetIndex].focus();
    }
}

/**
 * Setup focus management
 */
function setupFocusManagement() {
    // Return focus to trigger when modals close
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(function(modal) {
        let triggerElement = null;
        
        modal.addEventListener('show.bs.modal', function(e) {
            triggerElement = e.relatedTarget;
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            if (triggerElement) {
                triggerElement.focus();
            }
        });
    });
}

/**
 * Initialize animations
 */
function initializeAnimations() {
    // Intersection Observer for scroll animations
    if ('IntersectionObserver' in window) {
        setupScrollAnimations();
    }
    
    // Loading states
    setupLoadingStates();
}

/**
 * Setup scroll animations
 */
function setupScrollAnimations() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    animateElements.forEach(function(el) {
        observer.observe(el);
    });
}

/**
 * Setup loading states
 */
function setupLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                showButtonLoading(submitBtn);
            }
        });
    });
}

/**
 * Show button loading state
 */
function showButtonLoading(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    
    // Store original text to restore if needed
    button.dataset.originalText = originalText;
}

/**
 * Hide button loading state
 */
function hideButtonLoading(button) {
    button.disabled = false;
    button.innerHTML = button.dataset.originalText || 'Submit';
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
    const iconClass = type === 'error' ? 'fa-exclamation-triangle' : 
                     type === 'success' ? 'fa-check-circle' : 'fa-info-circle';
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="fas ${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container, .container-fluid');
    if (container) {
        const alertElement = document.createElement('div');
        alertElement.innerHTML = alertHtml;
        container.insertBefore(alertElement.firstElementChild, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            const alert = container.querySelector('.alert');
            if (alert) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            }
        }, 5000);
    }
}

/**
 * Utility functions
 */
const Utils = {
    /**
     * Debounce function
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    /**
     * Format date
     */
    formatDate: function(date, format = 'YYYY-MM-DD') {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day);
    },
    
    /**
     * Validate email format
     */
    isValidEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    /**
     * Generate random ID
     */
    generateId: function() {
        return Math.random().toString(36).substr(2, 9);
    }
};

// Export for use in other scripts
window.AstraZenecaApp = {
    showNotification,
    showButtonLoading,
    hideButtonLoading,
    Utils
};
