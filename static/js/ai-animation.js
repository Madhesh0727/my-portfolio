class AIDataStream {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.dataPackets = [];
        
        this.init();
    }
    
    init() {
        this.canvas.className = 'ai-data-stream';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '-1';
        this.canvas.style.opacity = '0.2';
        
        document.body.appendChild(this.canvas);
        
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        this.createParticles();
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        const isMobile = window.innerWidth < 768;
        const particleCount = isMobile ? 15 : 30;
        const packetCount = isMobile ? 3 : 5;
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 2 + 1,
                speedX: (Math.random() - 0.5) * 0.3,
                speedY: (Math.random() - 0.5) * 0.3
            });
        }
        
        for (let i = 0; i < packetCount; i++) {
            this.dataPackets.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                text: this.generateBinaryString(12),
                speed: Math.random() * 1.5 + 0.5,
                opacity: Math.random() * 0.4 + 0.1
            });
        }
    }
    
    generateBinaryString(length) {
        let result = '';
        for (let i = 0; i < length; i++) {
            result += Math.round(Math.random());
        }
        return result;
    }
    
    drawMatrixRain() {
        const isMobile = window.innerWidth < 768;
        const columnCount = isMobile ? 10 : 20;
        const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        
        this.ctx.font = '14px "Share Tech Mono", monospace';
        this.ctx.fillStyle = '#0f0';
        
        for (let i = 0; i < columnCount; i++) {
            const x = (i * 50) % this.canvas.width;
            const y = (Date.now() * 0.01 + i * 50) % (this.canvas.height + 50) - 50;
            
            this.ctx.globalAlpha = 0.2;
            this.ctx.fillText(chars[Math.floor(Math.random() * chars.length)], x, y);
        }
    }
    
    drawNeuralConnections() {
        this.ctx.strokeStyle = '#0f0';
        this.ctx.lineWidth = 0.5;
        
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 70) {
                    this.ctx.globalAlpha = 0.1 * (1 - distance / 70);
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(p => {
            p.x += p.speedX;
            p.y += p.speedY;
            
            if (p.x < 0) p.x = this.canvas.width;
            if (p.x > this.canvas.width) p.x = 0;
            if (p.y < 0) p.y = this.canvas.height;
            if (p.y > this.canvas.height) p.y = 0;
            
            this.ctx.globalAlpha = 0.5;
            this.ctx.fillStyle = '#0f0';
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
        
        this.drawNeuralConnections();
        this.drawMatrixRain();
        
        this.dataPackets.forEach(packet => {
            packet.y += packet.speed;
            
            if (packet.y > this.canvas.height) {
                packet.y = 0;
                packet.x = Math.random() * this.canvas.width;
            }
            
            this.ctx.globalAlpha = packet.opacity;
            this.ctx.font = '12px "Share Tech Mono", monospace';
            this.ctx.fillStyle = '#0f0';
            this.ctx.fillText(packet.text, packet.x, packet.y);
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AIDataStream();
});