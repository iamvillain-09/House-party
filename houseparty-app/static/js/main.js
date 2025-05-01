document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animation library
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Navbar color change on scroll
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            }
        });
    });
    
    // Set active nav item on scroll
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', function() {
        let current = '';
        const navHeight = navbar.offsetHeight;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - navHeight - 100;
            const sectionHeight = section.offsetHeight;
            
            if (window.pageYOffset >= sectionTop) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // Countdown Timer
    function countdownTimer() {
        // Set the target date (e.g., next Friday 9 PM)
        const now = new Date();
        let targetDate = new Date();
        
        // Set to next Friday (day 5)
        targetDate.setDate(now.getDate() + ((5 + 7 - now.getDay()) % 7));
        targetDate.setHours(21, 0, 0, 0); // 9 PM
        
        // If today is Friday and it's before 9 PM, set to today
        if (now.getDay() === 5 && now.getHours() < 21) {
            targetDate = new Date();
            targetDate.setHours(21, 0, 0, 0);
        }
        
        // If today is Friday and it's past 9 PM, set to next Friday
        if (now.getDay() === 5 && now.getHours() >= 21) {
            targetDate.setDate(now.getDate() + 7);
        }
        
        const countdownElement = document.getElementById('countdown');
        if (!countdownElement) return;
        
        function updateCountdown() {
            const now = new Date();
            const diff = targetDate - now;
            
            if (diff <= 0) {
                // If event has started, reset to next week
                targetDate.setDate(targetDate.getDate() + 7);
                updateCountdown();
                return;
            }
            
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);
            
            document.getElementById('countdown-days').textContent = days.toString().padStart(2, '0');
            document.getElementById('countdown-hours').textContent = hours.toString().padStart(2, '0');
            document.getElementById('countdown-minutes').textContent = minutes.toString().padStart(2, '0');
            document.getElementById('countdown-seconds').textContent = seconds.toString().padStart(2, '0');
        }
        
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
    
    countdownTimer();
    
    // Form submission with FormSpree
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const formAction = this.getAttribute('action');
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalButtonText = submitBtn.textContent;
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            
            fetch(formAction, {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                // Show success message
                document.getElementById('formSuccess').classList.remove('d-none');
                contactForm.reset();
                submitBtn.textContent = originalButtonText;
                submitBtn.disabled = false;
                
                // Hide success message after 5 seconds
                setTimeout(() => {
                    document.getElementById('formSuccess').classList.add('d-none');
                }, 5000);
            })
            .catch(error => {
                // Show error message
                document.getElementById('formError').classList.remove('d-none');
                submitBtn.textContent = originalButtonText;
                submitBtn.disabled = false;
                
                // Hide error message after 5 seconds
                setTimeout(() => {
                    document.getElementById('formError').classList.add('d-none');
                }, 5000);
            });
        });
    }
});
