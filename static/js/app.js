document.addEventListener('DOMContentLoaded', () => {
  // Smooth animations for auth state changes
  const authLinks = document.querySelectorAll('.auth-links a');
  authLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.target.parentElement.animate([
        { opacity: 1, transform: 'scale(1)' },
        { opacity: 0.8, transform: 'scale(0.98)' }
      ], { duration: 200 });
    });
  });

  // Dynamic background for auth forms
  if (window.location.pathname.includes('/auth/')) {
    document.body.style.background = 
      'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)';
  }
});
