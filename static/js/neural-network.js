// Neural Network Visualization
class NeuralNetworkVis {
    constructor() {
        this.layers = [4, 8, 12, 8, 4]; // Network architecture
        this.nodes = [];
        this.connections = [];
        this.activations = [];
        
        this.init();
    }
    
    init() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.className = 'neural-network-vis';
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '-1';
        this.canvas.style.opacity = '0.1';
        
        document.body.appendChild(this.canvas);
        
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        this.createNetwork();
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createNetwork() {
        const layerSpacing = this.canvas.width / (this.layers.length + 1);
        
        // Create nodes
        this.layers.forEach((nodeCount, layerIndex) => {
            const layerNodes = [];
            const nodeSpacing = this.canvas.height / (nodeCount + 1);
            const x = (layerIndex + 1) * layerSpacing;
            
            for (let i = 0; i < nodeCount; i++) {
                const y = (i + 1) * nodeSpacing;
                layerNodes.push({
                    x: x,
                    y: y,
                    activation: 0,
                    targetActivation: Math.random()
                });
            }
            
            this.nodes.push(layerNodes);
        });
        
        // Create connections between layers
        for (let l = 0; l < this.nodes.length - 1; l++) {
            const currentLayer = this.nodes[l];
            const nextLayer = this.nodes[l + 1];
            
            currentLayer.forEach((node, i) => {
                nextLayer.forEach((nextNode, j) => {
                    this.connections.push({
                        from: node,
                        to: nextNode,
                        weight: Math.random() * 2 - 1,
                        active: false
                    });
                });
            });
        }
    }
    
    updateActivations() {
        // Simulate forward pass
        this.nodes.forEach((layer, l) => {
            layer.forEach(node => {
                if (l === 0) {
                    // Input layer - random activation
                    node.targetActivation = Math.random();
                } else {
                    // Hidden/Output layers - compute from previous layer
                    let sum = 0;
                    this.nodes[l - 1].forEach(prevNode => {
                        const connection = this.connections.find(c => 
                            c.from === prevNode && c.to === node
                        );
                        if (connection) {
                            sum += prevNode.activation * connection.weight;
                        }
                    });
                    node.targetActivation = 1 / (1 + Math.exp(-sum)); // Sigmoid
                }
                
                // Smoothly transition to target activation
                node.activation += (node.targetActivation - node.activation) * 0.1;
                
                // Update connections activation
                this.connections.forEach(conn => {
                    if (conn.to === node) {
                        conn.active = Math.random() < Math.abs(conn.to.activation);
                    }
                });
            });
        });
    }
    
    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections first (so they appear behind nodes)
        this.connections.forEach(conn => {
            if (conn.active) {
                this.ctx.beginPath();
                this.ctx.moveTo(conn.from.x, conn.from.y);
                this.ctx.lineTo(conn.to.x, conn.to.y);
                
                // Gradient based on weight
                const gradient = this.ctx.createLinearGradient(
                    conn.from.x, conn.from.y, 
                    conn.to.x, conn.to.y
                );
                
                if (conn.weight > 0) {
                    gradient.addColorStop(0, '#0f0');
                    gradient.addColorStop(1, '#0f0');
                } else {
                    gradient.addColorStop(0, '#f0f');
                    gradient.addColorStop(1, '#f0f');
                }
                
                this.ctx.strokeStyle = gradient;
                this.ctx.lineWidth = Math.abs(conn.weight) * 2;
                this.ctx.globalAlpha = 0.3;
                this.ctx.stroke();
            }
        });
        
        // Draw nodes
        this.nodes.forEach(layer => {
            layer.forEach(node => {
                const radius = 5 + node.activation * 10;
                
                // Glow effect
                this.ctx.shadowColor = '#0f0';
                this.ctx.shadowBlur = 15 * node.activation;
                
                this.ctx.beginPath();
                this.ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
                
                // Gradient fill
                const gradient = this.ctx.createRadialGradient(
                    node.x, node.y, 0,
                    node.x, node.y, radius * 2
                );
                gradient.addColorStop(0, '#0f0');
                gradient.addColorStop(1, 'transparent');
                
                this.ctx.fillStyle = gradient;
                this.ctx.globalAlpha = 0.5 + node.activation * 0.3;
                this.ctx.fill();
                
                // Reset shadow
                this.ctx.shadowBlur = 0;
            });
        });
    }
    
    animate() {
        this.updateActivations();
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new NeuralNetworkVis();
});