// API Form Integration Fix for APEX Digital
(function() {
  const API_URL = '/contact-form';
  
  function interceptForm() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      if (form.dataset.apiConnected) return;
      form.dataset.apiConnected = 'true';
      
      form.addEventListener('submit', async function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Collect form data
        const formData = new FormData(form);
        const data = {};
        
        // Get all inputs
        form.querySelectorAll('input, select, textarea').forEach(field => {
          if (field.name) data[field.name] = field.value;
        });
        
        // Map fields to API format
        const apiData = {
          name: data.name || '',
          email: data.email || '',
          company: data.company || '',
          website: data.website || '',
          industry: data.industry || '',
          budget: data.budget || '',
          service_interest: data.services || '',
          message: data.message || ''
        };
        
        try {
          const btn = form.querySelector('button[type="submit"]');
          if (btn) {
            btn.disabled = true;
            btn.innerHTML = 'Sending...';
          }
          
          const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(apiData)
          });
          
          if (response.ok) {
            // Trigger React success state
            const submitEvent = new Event('submit', { bubbles: true });
            Object.defineProperty(submitEvent, 'defaultPrevented', { value: false });
            
            // Find React form handler and trigger success
            const checkCircle = document.querySelector('.bg-emerald-100');
            if (checkCircle) {
              // Already on success page
              return;
            }
            
            // Simulate successful submission for React
            form.style.display = 'none';
            const parent = form.closest('.bg-apex-offwhite');
            if (parent) {
              parent.innerHTML = `
                <div class="text-center py-12">
                  <div class="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg class="w-10 h-10 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <h2 class="text-3xl font-bold text-apex-navy mb-4">Thank You!</h2>
                  <p class="text-apex-text/70 mb-6">We've received your information and our team is already analyzing your business. You'll receive your free marketing audit within 24 hours.</p>
                  <div class="flex items-center justify-center gap-2 text-apex-blue">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                    <span>Check your inbox soon!</span>
                  </div>
                </div>
              `;
            }
          } else {
            alert('Error submitting form. Please try again.');
            if (btn) {
              btn.disabled = false;
              btn.innerHTML = 'Get My Free Marketing Audit →';
            }
          }
        } catch (error) {
          console.error('Form error:', error);
          alert('Network error. Please check your connection.');
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = 'Get My Free Marketing Audit →';
          }
        }
      }, true);
    });
  }
  
  // Run on load and periodically check for dynamically added forms
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', interceptForm);
  } else {
    interceptForm();
  }
  
  setInterval(interceptForm, 1000);
})();
