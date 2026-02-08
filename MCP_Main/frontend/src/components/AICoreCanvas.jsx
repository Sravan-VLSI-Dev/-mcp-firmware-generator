import React, { Suspense, useEffect, useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Line } from "@react-three/drei";
import { easing } from "maath";
import { useMotionValue, useSpring } from "framer-motion";
import { useMediaQuery } from "react-responsive";
import CanvasLoader from "./CanvasLoader";

function AICore() {
  const group = useRef(null);
  const ring = useRef(null);
  const isMobile = useMediaQuery({ maxWidth: 768 });
  const startY = useMotionValue(2.8);
  const springY = useSpring(startY, { stiffness: 120, damping: 18 });

  useEffect(() => {
    startY.set(0);
  }, [startY]);

  const nodes = useMemo(
    () =>
      [
        [1.1, 0.2, 0.4],
        [-0.9, -0.3, 0.6],
        [0.5, 0.8, -0.5],
        [-0.6, 0.9, -0.2],
        [0.0, -1.0, 0.2]
      ],
    []
  );

  const lines = useMemo(
    () => nodes.map((n) => [n, [0, 0, 0]]),
    [nodes]
  );

  useFrame((state, delta) => {
    if (!group.current) return;
    const auto = state.clock.getElapsedTime() * 0.35;
    const targetRot = [state.pointer.y * 0.2, auto + state.pointer.x * 0.3, 0];
    easing.damp3(group.current.rotation, targetRot, 0.6, delta);
    group.current.position.y = springY.get();
    if (ring.current) {
      ring.current.rotation.z += delta * 0.6;
    }
  });

  return (
    <group ref={group} scale={isMobile ? 0.85 : 1}>
      <Float speed={1.2} rotationIntensity={0.5} floatIntensity={0.6}>
        <mesh>
          <icosahedronGeometry args={[0.55, 1]} />
          <meshStandardMaterial color="#7dd3fc" roughness={0.12} metalness={0.8} emissive="#38bdf8" emissiveIntensity={0.9} />
        </mesh>
        <mesh>
          <sphereGeometry args={[0.9, 32, 32]} />
          <meshStandardMaterial color="#0f172a" transparent opacity={0.18} emissive="#6366f1" emissiveIntensity={0.35} />
        </mesh>
        <mesh ref={ring}>
          <torusGeometry args={[1.05, 0.04, 16, 120]} />
          <meshStandardMaterial color="#22d3ee" emissive="#22d3ee" emissiveIntensity={1.2} />
        </mesh>
        {nodes.map((pos, idx) => (
          <mesh key={idx} position={pos}>
            <sphereGeometry args={[0.08, 18, 18]} />
            <meshStandardMaterial color="#7dd3fc" emissive="#38bdf8" emissiveIntensity={0.4} />
          </mesh>
        ))}
        {lines.map((line, idx) => (
          <Line key={idx} points={line} color="#60a5fa" lineWidth={1.4} />
        ))}
        <mesh position={[0, -0.85, 0]}>
          <boxGeometry args={[0.9, 0.2, 0.9]} />
          <meshStandardMaterial color="#0b1120" roughness={0.2} metalness={0.4} />
        </mesh>
        <mesh position={[0.75, 0.35, -0.5]}>
          <boxGeometry args={[0.35, 0.15, 0.35]} />
          <meshStandardMaterial color="#1e293b" roughness={0.2} metalness={0.45} />
        </mesh>
      </Float>
    </group>
  );
}

export default function AICoreCanvas() {
  return (
    <div className="h-[380px] w-full md:h-[460px]">
      <Canvas
        camera={{ position: [0, 0.4, 4], fov: 45 }}
        gl={{ antialias: true, alpha: true }}
      >
        <ambientLight intensity={1.1} />
        <pointLight position={[4, 5, 6]} intensity={1.6} color="#60a5fa" />
        <pointLight position={[-5, -4, -4]} intensity={1.3} color="#22d3ee" />
        <pointLight position={[0, 0, 3]} intensity={0.9} color="#c7d2fe" />
        <Suspense fallback={<CanvasLoader label="Booting Core" />}>
          <AICore />
        </Suspense>
      </Canvas>
    </div>
  );
}
