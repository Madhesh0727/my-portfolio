// Matrix Rain Effect
class MatrixRain {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.columns = [];
        this.characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        
        this.init();
    }
    
    init() {
        this.canvas.className = 'matrix-rain';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '-1';
        this.canvas.style.opacity = '0.15';
        
        document.body.appendChild(this.canvas);
        
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        const columnCount = Math.floor(this.canvas.width / 20);
        this.columns = [];
        
        for (let i = 0; i < columnCount; i++) {
            this.columns.push({
                y: Math.random() * this.canvas.height,
                speed: 2 + Math.random() * 5,
                chars: []
            });
            
            // Generate random characters for this column
            for (let j = 0; j < 20; j++) {
                this.columns[i].chars.push({
                    char: this.characters[Math.floor(Math.random() * this.characters.length)],
                    opacity: 0.1 + Math.random() * 0.5
                });
            }
        }
    }
    
    animate() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.ctx.font = '15px "Share Tech Mono", monospace';
        
        this.columns.forEach((column, i) => {
            const x = i * 20;
            
            for (let j = 0; j < column.chars.length; j++) {
                const y = column.y - j * 20;
                const char = column.chars[j];
                
                if (y > 0 && y < this.canvas.height) {
                    // Gradient from bright to dim
                    const brightness = Math.max(0, 1 - j / column.chars.length);
                    
                    if (j === 0) {
                        this.ctx.fillStyle = `rgba(255, 255, 255, ${brightness})`;
                    } else {
                        this.ctx.fillStyle = `rgba(0, 255, 0, ${brightness * 0.5})`;
                    }
                    
                    this.ctx.fillText(char.char, x, y);
                }
            }
            
            column.y += column.speed;
            
            // Reset when off screen
            if (column.y > this.canvas.height + column.chars.length * 20) {
                column.y = -column.chars.length * 20;
            }
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new MatrixRain();
});