// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the prediction form
    const predictionForm = document.getElementById('prediction-form');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePredictionSubmit);
    }

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Add input validation for numeric fields
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('input', validateNumericInput);
    });
});

// Handle form submission
async function handlePredictionSubmit(e) {
    e.preventDefault();

    // Show loading state
    const submitButton = e.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    submitButton.disabled = true;

    try {
        // Get form data
        const formData = new FormData(e.target);
        
        // Make prediction request
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        // Show result in modal
        showPredictionResult(result);
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred while making the prediction. Please try again.');
    } finally {
        // Reset button state
        submitButton.innerHTML = originalButtonText;
        submitButton.disabled = false;
    }
}

// Show prediction result in modal
function showPredictionResult(result) {
    const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    const resultIcon = document.getElementById('result-icon');
    const predictionText = document.getElementById('prediction-text');
    const probabilityText = document.getElementById('probability-text');

    // Set icon based on prediction
    if (result.status === 'success') {
        resultIcon.innerHTML = '<i class="fas fa-check-circle text-success"></i>';
        resultIcon.className = 'success fade-in';
    } else {
        resultIcon.innerHTML = '<i class="fas fa-exclamation-circle text-danger"></i>';
        resultIcon.className = 'danger fade-in';
    }

    // Set prediction text
    predictionText.textContent = result.prediction;
    predictionText.className = `text-${result.status} fade-in`;

    // Set probability text
    probabilityText.textContent = `Probability To Leave : ${result.probability}%`;
    probabilityText.className = 'lead fade-in';

    // Show modal
    resultModal.show();
}

// Show error message
function showError(message) {
    const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    const resultIcon = document.getElementById('result-icon');
    const predictionText = document.getElementById('prediction-text');
    const probabilityText = document.getElementById('probability-text');

    resultIcon.innerHTML = '<i class="fas fa-times-circle text-danger"></i>';
    resultIcon.className = 'danger fade-in';
    predictionText.textContent = 'Error';
    predictionText.className = 'text-danger fade-in';
    probabilityText.textContent = message;
    probabilityText.className = 'lead fade-in';

    resultModal.show();
}

// Validate numeric inputs
function validateNumericInput(e) {
    const input = e.target;
    
    // Work-Life Balance validation (1-4)
    if (input.name === 'work_life_balance') {
        if (input.value < 1) input.value = 1;
        if (input.value > 4) input.value = 4;
    }
    
    // General validation for positive numbers
    if (input.value < 0) input.value = 0;
    
    // Specific validations
    switch(input.name) {
        case 'age':
            if (input.value > 100) input.value = 100;
            break;
        case 'job_level':
            if (input.value > 5) input.value = 5;
            break;
        case 'stock_option_level':
            if (input.value > 3) input.value = 3;
            break;
    }
}

// Add smooth scrolling to all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add animation when elements come into view
const animateOnScroll = function() {
    const elements = document.querySelectorAll('.feature-box');
    
    elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if(elementPosition < screenPosition) {
            element.classList.add('fade-in');
        }
    });
}

window.addEventListener('scroll', animateOnScroll);