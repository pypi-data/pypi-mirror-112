import * as THREE from '/js/three.module.js';

$(function () {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 600, 0.1, 1000);

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, 600);
    document.body.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 5;

    const animate = function () {
        requestAnimationFrame(animate);

        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;

        renderer.render(scene, camera);
    };

    animate();
});