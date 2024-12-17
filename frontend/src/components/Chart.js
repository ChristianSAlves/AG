import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function Chart({ history }) {
  const labels = history.map((_, index) => `Geração ${index}`);
  const bestFitness = history.map((h) => h.best_fitness);
  const avgFitness = history.map((h) => h.average_fitness); // A aptidão média

  // Dados para o gráfico da Melhor Aptidão
  const bestFitnessData = {
    labels,
    datasets: [
      {
        label: "Melhor Aptidão",
        data: bestFitness,
        borderColor: "red",
        fill: false,
      },
    ],
  };

  // Dados para o gráfico da Aptidão Média
  const avgFitnessData = {
    labels,
    datasets: [
      {
        label: "Aptidão Média",
        data: avgFitness,
        borderColor: "blue",
        fill: false,
      },
    ],
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Progresso das Gerações</h2>

      <div style={{ marginBottom: "40px" }}>
        <h3>Melhor Aptidão</h3>
        <Line data={bestFitnessData} />
      </div>

      <div>
        <h3>Aptidão Média</h3>
        <Line data={avgFitnessData} />
      </div>
    </div>
  );
}
