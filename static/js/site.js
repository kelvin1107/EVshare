// EVshare — shared front-end behavior for the Django templates.
// Search results, bookings, and listings are rendered server-side
// by Django views — this file only handles UI interactions.

document.addEventListener('DOMContentLoaded', () => {
  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('mainNav');

  if (navToggle && mainNav) {
    navToggle.addEventListener('click', () => {
      const isOpen = mainNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen);
      navToggle.classList.toggle('open');
    });
  }
});
