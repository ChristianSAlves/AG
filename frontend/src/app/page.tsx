"use client";
import { useState } from "react";
import dynamic from "next/dynamic";

// Carrega o componente Chart.js dinamicamente (evita SSR)
const Chart = dynamic(() => import("../components/Chart"), { ssr: false });

export default function Home() {
  const [generations, setGenerations] = useState<number>(100);
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const runAlgorithm = async () => {
    setLoading(true);
    setError(null);
  
    try {
      const response = await fetch("http://127.0.0.1:5000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ generations }),
      });
  
      const data = await response.json();
      console.log("Dados recebidos:", data);
  
      if (data.history && Array.isArray(data.history)) {
        setHistory(data.history);
      } else {
        throw new Error("Histórico não encontrado na resposta.");
      }
    } catch (err: any) {
      console.error(err.message);
      setError("Falha ao conectar ao servidor ou processar a resposta.");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div style={{ padding: "20px" }}>
      <h1>Algoritmo Genético</h1>
      <div>
        <label>
          Número de Gerações:{" "}
          <input
            type="number"
            value={generations}
            onChange={(e) => setGenerations(Number(e.target.value) || 0)}
            style={{ margin: "10px" }}
          />
        </label>
        <button onClick={runAlgorithm} disabled={loading}>
          {loading ? "Executando..." : "Executar"}
        </button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {history.length > 0 ? (
        <Chart history={history} />
      ) : (
        <p>Nenhum dado disponível. Execute o algoritmo.</p>
      )}
    </div>
  );
}
