import { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { useTexture } from "@react-three/drei";
import boardyHeadImage from "@/assets/boardy-head.png";
import matchaCupImage from "@/assets/matcha-cup-new.png";

type PostType = "performative" | "serious" | "cluely" | "boardy";

// Matcha Cup for Performative
function MatchaCup({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const texture = useTexture(matchaCupImage);
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.5;
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + position[0]) * 0.3;
    }
  });

  return (
    <mesh ref={meshRef} position={position}>
      <planeGeometry args={[1.5, 1.5]} />
      <meshStandardMaterial map={texture} transparent opacity={0.9} side={THREE.DoubleSide} />
    </mesh>
  );
}

// Nerd Glasses for Serious
function NerdGlasses({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Group>(null);
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.3;
      meshRef.current.rotation.y += delta * 0.4;
    }
  });

  return (
    <group ref={meshRef} position={position}>
      <mesh position={[-0.6, 0, 0]}>
        <torusGeometry args={[0.4, 0.08, 16, 32]} />
        <meshStandardMaterial color="#333333" transparent opacity={0.8} />
      </mesh>
      <mesh position={[0.6, 0, 0]}>
        <torusGeometry args={[0.4, 0.08, 16, 32]} />
        <meshStandardMaterial color="#333333" transparent opacity={0.8} />
      </mesh>
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[0.3, 0.05, 0.05]} />
        <meshStandardMaterial color="#333333" transparent opacity={0.8} />
      </mesh>
    </group>
  );
}

// Conference Box for Boardy
function BoardyBox({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const texture = useTexture(boardyHeadImage);
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.4;
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  return (
    <mesh ref={meshRef} position={position}>
      <boxGeometry args={[1.5, 1.5, 1.5]} />
      <meshStandardMaterial map={texture} transparent opacity={0.9} />
    </mesh>
  );
}

// Question Mark for Cluely
function QuestionMark({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Group>(null);
  
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.z += delta * 0.5;
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + position[0]) * 0.4;
    }
  });

  return (
    <group ref={meshRef} position={position}>
      <mesh position={[0, 0.3, 0]}>
        <torusGeometry args={[0.4, 0.15, 16, 32, Math.PI * 1.5]} />
        <meshStandardMaterial color="#FFD700" transparent opacity={0.8} />
      </mesh>
      <mesh position={[0, -0.5, 0]}>
        <sphereGeometry args={[0.15, 32, 32]} />
        <meshStandardMaterial color="#FFD700" transparent opacity={0.8} />
      </mesh>
    </group>
  );
}

function PerformativeScene() {
  return (
    <>
      <MatchaCup position={[-3, 2, -2]} />
      <MatchaCup position={[3, -1, -3]} />
      <MatchaCup position={[4, 3, -4]} />
      <MatchaCup position={[-4, -2, -3]} />
      <MatchaCup position={[0, 0, -5]} />
    </>
  );
}

function SeriousScene() {
  return (
    <>
      <NerdGlasses position={[-3, 2, -2]} />
      <NerdGlasses position={[3, -1, -3]} />
      <NerdGlasses position={[4, 3, -4]} />
      <NerdGlasses position={[-4, -2, -3]} />
      <NerdGlasses position={[0, 0, -5]} />
    </>
  );
}

function BoardyScene() {
  return (
    <>
      <BoardyBox position={[-3, 2, -2]} />
      <BoardyBox position={[3, -1, -3]} />
      <BoardyBox position={[4, 3, -4]} />
      <BoardyBox position={[-4, -2, -3]} />
      <BoardyBox position={[0, 0, -5]} />
    </>
  );
}

function CluelyScene() {
  return (
    <>
      <QuestionMark position={[-3, 2, -2]} />
      <QuestionMark position={[3, -1, -3]} />
      <QuestionMark position={[4, 3, -4]} />
      <QuestionMark position={[-4, -2, -3]} />
      <QuestionMark position={[0, 0, -5]} />
    </>
  );
}

function Scene({ postType }: { postType: PostType }) {
  return (
    <>
      <ambientLight intensity={0.8} />
      <directionalLight position={[5, 5, 5]} intensity={1.5} />
      <pointLight position={[-5, -5, -5]} intensity={1} />
      
      {postType === "performative" && <PerformativeScene />}
      {postType === "serious" && <SeriousScene />}
      {postType === "boardy" && <BoardyScene />}
      {postType === "cluely" && <CluelyScene />}
    </>
  );
}

const Scene3D = ({ postType }: { postType: PostType }) => {
  return (
    <div className="absolute inset-0 z-0 pointer-events-none">
      <Canvas
        camera={{ position: [0, 0, 10], fov: 50 }}
        style={{ background: 'transparent' }}
      >
        <Scene postType={postType} />
      </Canvas>
    </div>
  );
};

export default Scene3D;
