import React, { Suspense, useMemo, useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Line } from "@react-three/drei";
import CanvasLoader from "./CanvasLoader";

function Graph() {
  const group = useRef(null);
  const [hovered, setHovered] = useState(null);
  const nodes = useMemo(
    () => [
      [0, 0.6, 0],
      [-0.7, 0.1, 0.2],
      [0.7, 0.1, -0.2],
      [-0.3, -0.7, 0.1],
      [0.3, -0.7, -0.1]
    ],
    []
  );

  const edges = useMemo(
    () => [
      [nodes[0], nodes[1]],
      [nodes[0], nodes[2]],
      [nodes[1], nodes[3]],
      [nodes[2], nodes[4]],
      [nodes[3], nodes[4]]
    ],
    [nodes]
  );

  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.15;
  });

  return (
    <group ref={group}>
      {edges.map((edge, idx) => (
        <Line
          key={idx}
          points={edge}
          color={hovered ? "#22d3ee" : "#475569"}
          lineWidth={1.2}
        />
      ))}
      {nodes.map((pos, idx) => (
        <mesh
          key={idx}
          position={pos}
          onPointerOver={() => setHovered(idx)}
          onPointerOut={() => setHovered(null)}
        >
          <sphereGeometry args={[0.08, 16, 16]} />
          <meshStandardMaterial
            color={hovered === idx ? "#38bdf8" : "#94a3b8"}
            emissive={hovered === idx ? "#38bdf8" : "#0f172a"}
            emissiveIntensity={0.4}
          />
        </mesh>
      ))}
    </group>
  );
}

export default function SystemGraphCanvas() {
  return (
    <div className="h-56 w-full">
      <Canvas camera={{ position: [0, 0, 2.5], fov: 50 }}>
        <ambientLight intensity={0.7} />
        <pointLight position={[3, 3, 3]} intensity={0.8} />
        <Suspense fallback={<CanvasLoader label="Sync Graph" />}>
          <Graph />
        </Suspense>
      </Canvas>
    </div>
  );
}
