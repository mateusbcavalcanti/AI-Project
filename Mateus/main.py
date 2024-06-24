import random
import math

POPULATION_SIZE = 2
GENOME_LENGTH = 12
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
GENERATIONS = 200
GENOME_MEAN = 50


# TALVEZ MUDAR ISSO PARA O GENOMA INICIAL SER OS DADOS DO ANO ANTERIOR (!!???!!)
def random_genome(length, target_mean):
    array = [random.uniform(10, 200) for _ in range(length)]
    current_mean = sum(array) / len(array)

    adjustment_factor = target_mean / current_mean
    adjusted_array = [gene * adjustment_factor for gene in array]

    return adjusted_array


def init_population(POPULATION_SIZE, GENOME_LENGTH):
    return [
        random_genome(GENOME_LENGTH, GENOME_MEAN)
        for _ in range(POPULATION_SIZE)
    ]


def fitness(genome):
    x1 = genome[0]
    x2 = genome[1]
    Z = -math.exp(0.2 * math.sqrt((x1 - 1)**2 +
                                  (x2 - 1)**2)) + (math.cos(2 * x1) +
                                                   math.sin(2 * x1))

    #resto da funcao que ele mandou no email mas no local errado
    #offspring1 = [max(min(gene, 5.0), -5.0) for gene in offspring1]
    #offspring2 = [max(min(gene, 5.0), -5.0) for gene in offspring2]
    return Z


def select_parent(population, fitness_values):
    min_fitness = min(fitness_values)
    adjusted_fitness_values = [f - min_fitness + 1 for f in fitness_values]
    total_fitness = sum(adjusted_fitness_values)

    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness_value in zip(population, adjusted_fitness_values):
        current += fitness_value
        if current > pick:
            return individual

    return random.choice(population)


def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        crossover_point = random.randint(1, len(parent1) - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        offspring1, offspring2 = parent1, parent2
    return offspring1, offspring2


def mutate(genome):
    for i in range(len(genome)):
        if random.random() < MUTATION_RATE:
            genome[i] += random.uniform(-0.1, 0.1) * genome[i]
    return genome


def genetic_algorithm():
    population = init_population(POPULATION_SIZE, GENOME_LENGTH)
    print(f"população inicial: {population}\n\n")

    for generation in range(GENERATIONS):
        fitness_values = [fitness(genome) for genome in population]

        new_population = []

        for _ in range(POPULATION_SIZE // 2):
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)

            offspring1, offspring2 = crossover(parent1, parent2)

            new_population.extend([mutate(offspring1), mutate(offspring2)])

        population = new_population

        fitness_values = [fitness(genome) for genome in population]

        best_fitness = max(fitness_values)
        print(f"Geração {generation}: best fitness = {best_fitness}")

    best_index = fitness_values.index(max(fitness_values))
    best_solution = population[best_index]

    print(f"Melhor solução: {best_solution}")
    print(f"Melhor fitness: {fitness(best_solution)}")


if __name__ == '__main__':
    genetic_algorithm()
