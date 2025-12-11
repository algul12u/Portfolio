import * as dat from 'https://cdn.jsdelivr.net/npm/dat.gui@0.7.9/build/dat.gui.module.js';
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.150.1/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/loaders/GLTFLoader.js';
import { OBJLoader } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/loaders/OBJLoader.js';
import { Reflector } from 'https://cdn.jsdelivr.net/npm/three@0.150.1/examples/jsm/objects/Reflector.js';

// SCENE
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB);
scene.fog = new THREE.FogExp2(0xCCC8C4); 

// CAMERA
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 5000);
camera.position.set(950, 400, 30);

// RENDERER
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.shadowMap.enabled = true; 
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// CONTROLS
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.screenSpacePanning = false;
controls.maxDistance = 2000;
controls.minDistance = 50;
controls.target.set(0, 0, 0);

// Directional Light (Soleil)
const sunLight = new THREE.DirectionalLight(0xffddaa, 3);
sunLight.position.set(500, 500, -500);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 4096;
sunLight.shadow.mapSize.height = 4096;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 5000;
sunLight.shadow.camera.left = -1000;
sunLight.shadow.camera.right = 1000;
sunLight.shadow.camera.top = 1000;
sunLight.shadow.camera.bottom = -1000;
scene.add(sunLight);

// Lumière ambiante (éclaire toute la scène)
const ambientLight = new THREE.AmbientLight(0x404040, 2);
scene.add(ambientLight);

// Spotlight
const spotLight = new THREE.SpotLight(0xffffff, 5, 500, Math.PI / 6, 0.5, 2);
spotLight.position.set(250, 200, -50);
spotLight.castShadow = true;
scene.add(spotLight);

let boat1, boat2;
const loader = new GLTFLoader();

loader.load('modeles/old_bridge.glb', function (gltf) {
 const bridge = gltf.scene;

 bridge.traverse((node) => {
 if (node.isMesh) {
 node.castShadow = true;
 node.receiveShadow = true;
 }
 });

 scene.add(bridge);
 bridge.position.set(0, 100, 0);
 bridge.scale.set(0.5, 0.5, 0.5);
 bridge.rotation.y = Math.PI / 2;

 controls.target.copy(bridge.position);
 controls.update();
}, undefined, function (error) {
 console.error("Erreur de chargement du pont :", error);
});

loader.load('modeles/old_bridge.glb', function (gltf) {
 const bridge2 = gltf.scene;
 bridge2.traverse((node) => {
 if (node.isMesh) {
 node.castShadow = true;
 node.receiveShadow = true;
 }
 });

 scene.add(bridge2);
 bridge2.position.set(-950, 100, 0);
 bridge2.scale.set(0.5, 0.5, 0.5);
 bridge2.rotation.y = Math.PI / 2;

 controls.target.copy(bridge2.position);
 controls.update();
}, undefined, function (error) {
 console.error("Erreur de chargement du pont :", error);
});

loader.load('modeles/old_bridge.glb', function (gltf) {
 const bridge3 = gltf.scene;
 bridge3.traverse((node) => {
 if (node.isMesh) {
 node.castShadow = true;
 node.receiveShadow = true;
 }
 });

 scene.add(bridge3);
 bridge3.position.set(100, 100, 126);
 bridge3.scale.set(0.5, 0.5, 0.5);
 bridge3.rotation.y = Math.PI / -2;

 controls.target.copy(bridge3.position);
 controls.update();
}, undefined, function (error) {
 console.error("Erreur de chargement du pont :", error);
});

loader.load('modeles/old_bridge.glb', function (gltf) {
 const bridge4 = gltf.scene;
 bridge4.traverse((node) => {
 if (node.isMesh) {
 node.castShadow = true;
 node.receiveShadow = true;
 }
 });

 scene.add(bridge4);
 bridge4.position.set(-850, 100, 126);
 bridge4.scale.set(0.5, 0.5, 0.5);
 bridge4.rotation.y = Math.PI / -2;

 controls.target.copy(bridge4.position);
 controls.update();
}, undefined, function (error) {
 console.error("Erreur de chargement du pont :", error);
});

loader.load('modeles/bateau.glb', function (gltf) {
  boat1 = gltf.scene.clone();
  boat1.traverse((node) => {
    if (node.isMesh) {
      node.castShadow = true;
      node.receiveShadow = true;
    }
  });

  boat2 = gltf.scene.clone();
  boat2.traverse((node) => {
    if (node.isMesh) {
      node.castShadow = true;
      node.receiveShadow = true;
    }
  });

  boat1.position.set(-300, 1, -500);
  boat1.scale.set(0.3, 0.3, 0.3);

  boat2.position.set(-200, 1, -600);
  boat2.scale.set(0.3, 0.3, 0.3);
  boat2.rotation.y = Math.PI / 4;

  scene.add(boat1);
  scene.add(boat2);

}, undefined, function (error) {
  console.error("Erreur de chargement des bateaux :", error);
});

const textureLoader = new THREE.TextureLoader();
const groundTexture = textureLoader.load('textures/water2.jpg');
groundTexture.wrapS = groundTexture.wrapT = THREE.RepeatWrapping;
groundTexture.repeat.set(10, 10);

// Specular maps
function generateSpecularTexture(color, width = 128, height = 128) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext('2d');
  context.fillStyle = color;
  context.fillRect(0, 0, width, height);
  return new THREE.CanvasTexture(canvas);
}
const specularTexture = generateSpecularTexture('#555555');

const groundMaterial = new THREE.MeshPhongMaterial({
  map: groundTexture,
  specularMap: specularTexture,
  specular: new THREE.Color(0xffffff),
  shininess: 500,
  transparent: true,
  opacity: 0.7
});


const solidGround = new THREE.Mesh(
  new THREE.PlaneGeometry(10000, 10000, 100, 100),
  groundMaterial
);
solidGround.rotation.x = -Math.PI / 2;
solidGround.position.y = -2;
solidGround.receiveShadow = true;
scene.add(solidGround);

// Effet miroir  
const mirrorGeometry = new THREE.PlaneGeometry(10000, 10000);
const mirror = new Reflector(mirrorGeometry, {
  clipBias: 0.003, 
  textureWidth: window.innerWidth * window.devicePixelRatio,
  textureHeight: window.innerHeight * window.devicePixelRatio,
  color: 0x777777 
});

mirror.rotation.x = -Math.PI / 2;
mirror.position.y = -1.999;

mirror.material.transparent = true;
mirror.material.opacity = 0.5; 
mirror.renderOrder = 1;
scene.add(mirror);


const objLoader = new OBJLoader();
objLoader.load('modeles/scream/Scream 3D-bl.obj', function (obj) {
 const screamTexture = textureLoader.load('modeles/scream/Scream Texture.png');

 obj.traverse((child) => {
 if (child.isMesh) {
 child.material = new THREE.MeshBasicMaterial({ map: screamTexture });
 child.castShadow = true;
 child.receiveShadow = true;
 }
 });

 obj.position.set(250, -60, -30);
 obj.scale.set(20, 20, 20);
 obj.rotation.z = Math.PI / 2.5;
 obj.rotation.y = Math.PI / -5;

 spotLight.target = obj;
 scene.add(obj);
}, undefined, function (error) {
 console.error("Erreur de chargement du modèle Scream :", error);
});

const skyTexture = textureLoader.load('textures/skybox2.png');
const skyMaterial = new THREE.MeshBasicMaterial({
 map: skyTexture,
 side: THREE.BackSide
});
const skySphere = new THREE.Mesh(
 new THREE.SphereGeometry(3000, 32, 32),
 skyMaterial
);
skySphere.rotation.x = Math.PI / 2;
skySphere.rotation.z = Math.PI / -1;
scene.add(skySphere);

const spriteTexture = textureLoader.load('textures/sprite.png');
const spriteMaterial = new THREE.SpriteMaterial({ map: spriteTexture });
const sprite = new THREE.Sprite(spriteMaterial);
sprite.position.set(40, 160, -30);
sprite.scale.set(50, 100, 50);
scene.add(sprite);

const spriteTexture2 = textureLoader.load('textures/sprite2.png');
const spriteMaterial2 = new THREE.SpriteMaterial({ map: spriteTexture2 });
const sprite2 = new THREE.Sprite(spriteMaterial2);
sprite2.position.set(20, 160, 0);
sprite2.scale.set(50, 100, 50);
scene.add(sprite2);

const gui = new dat.GUI();
const cameraFolder = gui.addFolder("Zoom & Brouillard");
cameraFolder.add(camera, "fov", 10, 100).name("Zoom").onChange(() => {
 camera.updateProjectionMatrix();
});
cameraFolder.add(scene.fog, "density", 0, 0.0015).name("Brouillard");

const sunFolder = gui.addFolder("Soleil");
const sunColor = { color: sunLight.color.getHex() };
sunFolder.add(sunLight, "intensity", 0, 10).name("Intensité Soleil");
sunFolder.addColor(sunColor, "color").name("Couleur Soleil").onChange((value) => {
 sunLight.color.set(value);
});
sunFolder.add(sunLight.position, "x", -2000, 2000).name("Position X");
sunFolder.add(sunLight.position, "y", -2000, 2000).name("Position Y");
sunFolder.add(sunLight.position, "z", -2000, 2000).name("Position Z");

const ambientFolder = gui.addFolder("Lumière Ambiante");
const ambientColor = { color: ambientLight.color.getHex() };
ambientFolder.add(ambientLight, "intensity", 0, 5).name("Intensité Ambiante");
ambientFolder.addColor(ambientColor, "color").name("Couleur Ambiante").onChange((value) => {
 ambientLight.color.set(value);
});

const spotFolder = gui.addFolder("Spotlight sur Le Cri");
const spotColor = { color: spotLight.color.getHex() };
spotFolder.add(spotLight, "intensity", 0, 10).name("Intensité Spotlight");
spotFolder.addColor(spotColor, "color").name("Couleur Spotlight").onChange((value) => {
 spotLight.color.set(value);
});
spotFolder.add(spotLight.position, "x", -500, 500).name("Position X");
spotFolder.add(spotLight.position, "y", 50, 500).name("Position Y");
spotFolder.add(spotLight.position, "z", -500, 500).name("Position Z");

const specularFolder = gui.addFolder("Specular Maps");
specularFolder.add(groundMaterial, "shininess", 0, 1000).name("Shininess").onChange(() => {
  groundMaterial.needsUpdate = true;
});
specularFolder.addColor({ specular: groundMaterial.specular.getHex() }, "specular").name("Specular Color").onChange((value) => {
  groundMaterial.specular.setHex(value);
});

const groundParams = {
  color: 0xffffff 
};

const groundFolder = gui.addFolder("Eau");
groundFolder.addColor(groundParams, "color").name("Couleur Eau").onChange((value) => {
  groundMaterial.color.set(value);
});

function animate() {
  requestAnimationFrame(animate);
  controls.update();

  const t = Date.now() * 0.001; 

  const speed1 = 0.1;  
  const speed2 = 0.1; 

  if (boat1) {
    const radius1 = 100;
    const center1 = { x: -300, z: -500 };

    boat1.position.x = center1.x + radius1 * Math.cos(t * speed1);
    boat1.position.z = center1.z + radius1 * Math.sin(t * speed1);
    boat1.rotation.y = -t * speed1;
  }

  if (boat2) {
    const radius2 = 100;
    const center2 = { x: -200, z: -600 };

    boat2.position.x = center2.x + radius2 * Math.cos(-t * speed2);
    boat2.position.z = center2.z + radius2 * Math.sin(-t * speed2);
    boat2.rotation.y = t * speed2;
  }

  renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
 renderer.setSize(window.innerWidth, window.innerHeight);
 camera.aspect = window.innerWidth / window.innerHeight;
 camera.updateProjectionMatrix();
});
