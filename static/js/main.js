        // Navbar color change on scroll
        window.addEventListener('scroll', function() {
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Back to top button
        const backToTopButton = document.getElementById('back-to-top');

        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.style.display = 'block';
            } else {
                backToTopButton.style.display = 'none';
            }
        });

        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Activate animation when elements come into view
        const animateOnScroll = function() {
            const elements = document.querySelectorAll('.animate__animated');

            elements.forEach(function(element) {
                const position = element.getBoundingClientRect();

                // If the element is in the viewport
                if(position.top < window.innerHeight && position.bottom >= 0) {
                    // Get the animation class
                    const animationClass = Array.from(element.classList).find(className =>
                        className.startsWith('animate__') && className !== 'animate__animated'
                    );

                    // If it has 'animate__fadeIn' class and is not already visible
                    if(animationClass && !element.classList.contains('animated-in')) {
                        element.classList.add('animated-in');
                    }
                }
            });
        };

        window.addEventListener('scroll', animateOnScroll);
        // Trigger on page load
        window.addEventListener('load', animateOnScroll);
