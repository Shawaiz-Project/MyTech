// Page Loader functionality
document.addEventListener('DOMContentLoaded', function() {
  const loader = document.getElementById('page-loader');
  
  // Hide loader when page is fully loaded
  if (loader) {
    setTimeout(function() {
      loader.classList.add('hidden');
    }, 500);
  }
});

// Show loader on navigation
function showLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.remove('hidden');
  }
}

// Intercept all link clicks to show loader
document.addEventListener('click', function(e) {
  const link = e.target.closest('a');
  if (link && 
      link.href && 
      !link.href.includes('#') && 
      !link.target === '_blank' &&
      link.hostname === window.location.hostname &&
      !link.href.includes('javascript:')) {
    showLoader();
  }
});

// Show loader on form submissions
document.addEventListener('submit', function(e) {
  showLoader();
});
