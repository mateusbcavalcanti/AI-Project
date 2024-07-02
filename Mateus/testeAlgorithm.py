import random
import math
import numpy as np

POPULATION_SIZE = 50
GENOME_LENGTH = 12
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
GENERATIONS = 200
GENOME_MEAN = 50

horasPmes = np.array([744.00, 672.00, 744.00, 720.00, 744.00,720.00, 744.00, 744.00, 720.00, 744.00, 720.00, 744.00])
pld = np.array([242.72, 165.98, 109.02, 132.63, 218.70, 336.99,583.88, 583.88, 577.37, 249.36, 88.10, 66.67])  # em R$/MWh
energiaGerada1 = np.array([33.83, 34.90, 35.44, 35.11, 38.93, 44.30, 47.14, 46.71, 45.64, 43.22, 36.78, 37.58])  # em MWmed_mês
sazonalidadeC1 = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
sazonalidadeC2 = np.array([30, 30, 30, 30, 30, 30, 15, 10, 9, 10, 8, 8])
gfParque = 50
precoC1 = 120
flexibilidadeC1 = 0.3
receitaC1 = 0
precoC2 = 190
flexibilidadeC2 = 0
receitaC2 = 0
controle = True


def random_genome(length, target_mean):
    array = [random.uniform(10, 200) for _ in range(length)]
    current_mean = sum(array) / len(array)
    adjustment_factor = target_mean / current_mean
    adjusted_array = [gene * adjustment_factor for gene in array]
    return adjusted_array


def init_population(POPULATION_SIZE, GENOME_LENGTH):
    return [random_genome(GENOME_LENGTH, GENOME_MEAN) for _ in range(POPULATION_SIZE)]


def fitness(genome):
    if np.mean(genome) != GENOME_MEAN or any(genome[i] < (sazonalidadeC1[i] + sazonalidadeC2[i]) for i in range(GENOME_LENGTH)):
        return float('-inf')
    return calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2, genome, precoC1, precoC2, controle, receitaC1, receitaC2)


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


def adjust_genome(genome, target_mean):
    current_mean = np.mean(genome)
    adjustment_factor = target_mean / current_mean
    adjusted_genome = [gene * adjustment_factor for gene in genome]
    return adjusted_genome


def calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2, sazonalidadeMes, precoC1, precoC2, controle, receitaC1, receitaC2):
    if controle:
        receitaC1 = 0
        for i in range(12):
            econt = sazonalidadeC1[i] * horasPmes[i]
            eger = (sazonalidadeC1[i] / (sazonalidadeC1[i] +
                    sazonalidadeC2[i])) * (energiaGerada1[i] * horasPmes[i])
            receitaMes = (precoC1 * econt) + ((eger - econt) * pld[i])
            receitaC1 += receitaMes

        receitaC2 = 0
        for i in range(12):
            econt = sazonalidadeC2[i] * horasPmes[i]
            eger = (sazonalidadeC2[i] / (sazonalidadeC1[i] +
                    sazonalidadeC2[i])) * (energiaGerada1[i] * horasPmes[i])
            receitaMes = (precoC2 * econt) + ((eger - econt) * pld[i])
            receitaC2 += receitaMes

        receitaTotalEmpresa = receitaC1 + receitaC2
        return receitaTotalEmpresa
    return 0


def genetic_algorithm():
    population = init_population(POPULATION_SIZE, GENOME_LENGTH)
    # print(f"População inicial: {population}\n\n")

    for generation in range(GENERATIONS):
        fitness_values = [fitness(genome) for genome in population]
        new_population = []

        for _ in range(POPULATION_SIZE // 2):
            parent1 = select_parent(population, fitness_values)
            parent2 = select_parent(population, fitness_values)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.extend([mutate(offspring1), mutate(offspring2)])

        new_population = [adjust_genome(genome, GENOME_MEAN)
                          for genome in new_population]
        population = new_population

        fitness_values = [fitness(genome) for genome in population]

        best_fitness = max(fitness_values)
        print(f"Geração {generation}: melhor fitness = {best_fitness}")

        if best_fitness == float('-inf'):
            continue

        best_index = fitness_values.index(best_fitness)
        best_solution = population[best_index]

        if np.mean(best_solution) == GENOME_MEAN and all(best_solution[i] >= (sazonalidadeC1[i] + sazonalidadeC2[i]) for i in range(GENOME_LENGTH)):
            break

    best_index = fitness_values.index(max(fitness_values))
    best_solution = population[best_index]

    print(f"Melhor solução: {best_solution}")
    #print(f"Melhor fitness: {fitness(best_solution)}")
    media = np.mean(best_solution)
    print(f"Média: {media}")

    receitaTotalEmpresa = calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2, best_solution, precoC1, precoC2, controle, receitaC1, receitaC2)
    print(f"Receita total da empresa: {receitaTotalEmpresa}")


if __name__ == '__main__':
    genetic_algorithm()
