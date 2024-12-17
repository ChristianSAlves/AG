from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np

# Configurações do algoritmo genético
POPULATION_SIZE = 100
GENE_LENGTH = 10
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.01
INTERVAL = (0, 512)

# Função objetivo
def fitness_function(x):
    return np.sin(x) * np.sin(2 * x)

# Gerar população inicial
def generate_population():
    return np.random.randint(0, 2, (POPULATION_SIZE, GENE_LENGTH))

# Converter binário para decimal
def binary_to_decimal(binary):
    decimals = binary.dot(2**np.arange(binary.shape[1])[::-1])
    return INTERVAL[0] + (INTERVAL[1] - INTERVAL[0]) * decimals / (2**GENE_LENGTH - 1)

# Avaliar a população
def evaluate_population(population):
    decimals = binary_to_decimal(population)
    fitness_values = fitness_function(decimals)
    return fitness_values

# Seleção por roleta 
def roulette_wheel_selection(population, fitness_values):
    adjusted_fitness = fitness_values - fitness_values.min() + 1e-6  # Evitar zeros
    probabilities = adjusted_fitness / adjusted_fitness.sum()  # Normalizar
    indices = np.random.choice(len(population), size=len(population), p=probabilities)
    return population[indices]

# Crossover
def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        point = np.random.randint(1, GENE_LENGTH - 1)
        child1 = np.concatenate([parent1[:point], parent2[point:]])
        child2 = np.concatenate([parent2[:point], parent1[point:]])
        return child1, child2
    return parent1, parent2

# Mutação
def mutate(individual):
    for i in range(len(individual)):
        if np.random.rand() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
    return individual

# Nova geração
def create_new_generation(population, fitness_values):
    selected = roulette_wheel_selection(population, fitness_values)
    next_generation = []
    for i in range(0, len(selected), 2):
        parent1, parent2 = selected[i], selected[(i + 1) % len(selected)]
        child1, child2 = crossover(parent1, parent2)
        next_generation.append(mutate(child1))
        next_generation.append(mutate(child2))
    return np.array(next_generation[:POPULATION_SIZE])


app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
# Nova geração e cálculo de aptidão média
def run_algorithm():
    generations = int(request.json.get('generations', 100))
    population = generate_population()
    best_individual = None
    best_fitness = -np.inf
    history = []  # Iniciar o histórico

    for _ in range(generations):
        fitness_values = evaluate_population(population)
        max_fitness_idx = np.argmax(fitness_values)

        # Cálculo da melhor aptidão e individual
        if fitness_values[max_fitness_idx] > best_fitness:
            best_fitness = fitness_values[max_fitness_idx]
            best_individual = population[max_fitness_idx]

        # Calcular a aptidão média
        avg_fitness = fitness_values.mean()

        # Salvar o histórico de cada geração
        history.append({
            'generation': _,
            'best_individual': best_individual.tolist(),
            'best_fitness': float(best_fitness),
            'average_fitness': float(avg_fitness),  # Salvar a aptidão média
        })

        population = create_new_generation(population, fitness_values)

    best_value = binary_to_decimal(np.array([best_individual]))[0]
    return jsonify({
        'best_individual': best_individual.tolist(),
        'best_value': float(best_value),
        'best_fitness': float(best_fitness),
        'history': history 
    })


if __name__ == '__main__':
    app.run(debug=True)
