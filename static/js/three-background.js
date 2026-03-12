class NeuralNetworkBackground {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        
        this.nodes = [];
        this.connections = [];
        this.animationTime = 0;
        
        this.init();
        this.createNetwork();
        this.animate();
    }
    
    init() {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.setClearColor(0x000000, 0);
        document.getElementById('neural-bg').appendChild(this.renderer.domElement);
        
        this.camera.position.z = 30;
        
        window.addEventListener('resize', () => this.onWindowResize(), false);
    }
    
    createNetwork() {
        const isMobile = window.innerWidth < 768;
        const nodeCount = isMobile ? 25 : 50;
        const maxDistance = isMobile ? 10 : 15;
        const geometry = new THREE.SphereGeometry(0.3, 8, 8);
        
        for (let i = 0; i < nodeCount; i++) {
            const material = new THREE.MeshBasicMaterial({ 
                color: new THREE.Color(`hsl(${120 + Math.random() * 60}, 100%, 50%)`),
                transparent: true,
                opacity: 0.8
            });
            
            const sphere = new THREE.Mesh(geometry, material);
            
            const x = (Math.random() - 0.5) * 40;
            const y = (Math.random() - 0.5) * 40;
            const z = (Math.random() - 0.5) * 40;
            
            sphere.position.set(x, y, z);
            
            sphere.userData = {
                velocity: new THREE.Vector3(
                    (Math.random() - 0.5) * 0.02,
                    (Math.random() - 0.5) * 0.02,
                    (Math.random() - 0.5) * 0.02
                ),
                pulsePhase: Math.random() * Math.PI * 2
            };
            
            this.scene.add(sphere);
            this.nodes.push(sphere);
        }
        
        const connectionMaterial = new THREE.LineBasicMaterial({ 
            color: 0x00ff00,
            transparent: true,
            opacity: 0.2
        });
        
        for (let i = 0; i < this.nodes.length; i++) {
            for (let j = i + 1; j < this.nodes.length; j++) {
                const distance = this.nodes[i].position.distanceTo(this.nodes[j].position);
                
                if (distance < maxDistance) {
                    const points = [
                        this.nodes[i].position.x, this.nodes[i].position.y, this.nodes[i].position.z,
                        this.nodes[j].position.x, this.nodes[j].position.y, this.nodes[j].position.z
                    ];
                    
                    const connectionGeometry = new THREE.BufferGeometry();
                    connectionGeometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
                    const line = new THREE.Line(connectionGeometry, connectionMaterial);
                    
                    line.userData = {
                        node1: this.nodes[i],
                        node2: this.nodes[j]
                    };
                    
                    this.scene.add(line);
                    this.connections.push(line);
                }
            }
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        this.animationTime += 0.01;
        
        this.nodes.forEach((node) => {
            node.position.x += node.userData.velocity.x;
            node.position.y += node.userData.velocity.y;
            node.position.z += node.userData.velocity.z;
            
            ['x', 'y', 'z'].forEach(axis => {
                if (Math.abs(node.position[axis]) > 25) {
                    node.userData.velocity[axis] *= -1;
                }
            });
            
            const pulse = Math.sin(this.animationTime * 2 + node.userData.pulsePhase) * 0.3 + 0.7;
            node.material.opacity = pulse * 0.8;
            
            const scale = 1 + Math.sin(this.animationTime * 3 + node.userData.pulsePhase) * 0.2;
            node.scale.set(scale, scale, scale);
        });
        
        this.connections.forEach(conn => {
            const pos = conn.geometry.attributes.position;
            pos.array[0] = conn.userData.node1.position.x;
            pos.array[1] = conn.userData.node1.position.y;
            pos.array[2] = conn.userData.node1.position.z;
            pos.array[3] = conn.userData.node2.position.x;
            pos.array[4] = conn.userData.node2.position.y;
            pos.array[5] = conn.userData.node2.position.z;
            pos.needsUpdate = true;
            
            const distance = conn.userData.node1.position.distanceTo(conn.userData.node2.position);
            const opacity = Math.max(0, 0.3 - distance / 100);
            conn.material.opacity = opacity;
        });
        
        this.scene.rotation.y += 0.0005;
        this.scene.rotation.x += 0.0003;
        
        this.renderer.render(this.scene, this.camera);
    }
    
    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('neural-bg')) {
        new NeuralNetworkBackground();
    }
});