/**
 * AI-Based Career Path and Job Recommendation System
 * Client-Side JavaScript Utilities
 */

document.addEventListener('DOMContentLoaded', function() {
  // 1. Mobile Menu Toggle
  const mobileBtn = document.getElementById('mobileMenuBtn');
  const navMenu = document.getElementById('navMenu');

  if (mobileBtn && navMenu) {
    mobileBtn.addEventListener('click', function() {
      navMenu.classList.toggle('open');
      const icon = mobileBtn.querySelector('i');
      if (icon) {
        if (navMenu.classList.contains('open')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-xmark');
        } else {
          icon.classList.remove('fa-xmark');
          icon.classList.add('fa-bars');
        }
      }
    });
  }

  // 2. Drag & Drop Upload Zone Effects
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('resumeFileInput');

  if (dropZone && fileInput) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, function(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');
      }, false);
    });

    dropZone.addEventListener('drop', function(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        fileInput.files = files;
        const displayElem = document.getElementById('selectedFileName');
        if (displayElem) {
          displayElem.innerText = 'Selected: ' + files[0].name;
          displayElem.style.display = 'block';
        }
        const fileBtn = document.getElementById('fileSelectBtn');
        if (fileBtn) {
          fileBtn.innerHTML = '<i class="fa-solid fa-check"></i> ' + files[0].name;
        }
      }
    });
  }

  // 3. Auto-Dismiss Flash Alerts after 6 seconds
  const flashAlerts = document.querySelectorAll('.alert');
  if (flashAlerts.length > 0) {
    setTimeout(() => {
      flashAlerts.forEach(alert => {
        // Only auto-fade alerts inside flash-messages container
        if (alert.closest('.flash-messages')) {
          alert.style.transition = 'opacity 0.6s ease';
          alert.style.opacity = '0';
          setTimeout(() => alert.remove(), 600);
        }
      });
    }, 6000);
  }
});
