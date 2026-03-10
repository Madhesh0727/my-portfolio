document.addEventListener('DOMContentLoaded', () => {
    const typewriterElement = document.getElementById('typewriter');
    if (!typewriterElement) return;

    const words = [
        "Hi, I'm Madhesh",
        "Cybersecurity Student",
        "AI Builder"
    ];
    
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let typeSpeed = 100;
    
    function type() {
        // Current word
        const currentWord = words[wordIndex];
        
        // Check if deleting or typing
        if (isDeleting) {
            charIndex--;
            typeSpeed = 50; 
        } else {
            charIndex++;
            typeSpeed = 100;
        }
        
        // Update text
        typewriterElement.textContent = currentWord.substring(0, charIndex);
        
        // If word is complete
        if (!isDeleting && charIndex === currentWord.length) {
            typeSpeed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            typeSpeed = 500; // Pause before new word
        }
        
        setTimeout(type, typeSpeed);
    }
    
    // Start typing effect
    setTimeout(type, 1000);
});
