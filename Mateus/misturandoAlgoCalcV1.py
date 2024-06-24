import random
import math
import numpy as np

POPULATION_SIZE = 2
GENOME_LENGTH = 12
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
GENERATIONS = 200
GENOME_MEAN = 50



horasPmes = np.array([744.00, 672.00, 744.00, 720.00, 744.00, 720.00, 744.00, 744.00, 720.00, 744.00, 720.00, 744.00]) 
# diasPmes = np.array([31, 28, 31, 30, 31,30,31,31,30,31,30,31]) #dias para cada mes
pld = np.array([242.72, 165.98, 109.02, 132.63, 218.70, 336.99,583.88, 583.88, 577.37, 249.36, 88.10, 66.67])  # em R$/MWh
energiaGerada1 = np.array([33.83, 34.90, 35.44, 35.11, 38.93, 44.30,47.14, 46.71, 45.64, 43.22, 36.78, 37.58])  # em MWmed_mês
# energiaGerada2 = np.array([30.00, 28.00, 25.00, 20.00, 25.00, 26.00, 27.00, 30.00, 50.00, 70.00, 65.00, 30.00]) # em MWmed_mê
sazonalidadeC1 = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
sazonalidadeC2 = np.array([30, 30, 30, 30, 30, 30, 15, 10, 9, 10, 8, 8])
gfParque = 50
#sazonalidadeMes = np.array([50.00, 50.00, 50.00, 50.00, 50.00,50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00])  # MWmed
precoC1 = 120
flexibilidadeC1 = 0.3
receitaC1 = 0
precoC2 = 190
flexibilidadeC2 = 0
receitaC2 = 0
controle = True



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

#FUNCAO DO CALCULO DOS CONTRATOS
def calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2, sazonalidadeMes, precoC1, precoC2, controle, receitaC1, receitaC2):

    # for i in range(12):
    #     if (sazonalidadeMes[i] < (sazonalidadeC1[i] + sazonalidadeC2[i])):
    #         controle = False
    #         print(
    #             f"A sonalidade do mes {i+1} eh menor do que a soma da energia entregue nos contratos")

    # # variavel para armazenar a receita a cada mes
    # receitaMes = 0

    if (controle):
        # CALCULO DO PRIMEIRO CONTRATO
        for i in range(12):
            # energia contratada
            econt = sazonalidadeC1[i] * horasPmes[i]
            # calculo do percentual da energia gerada que pega o proporcional do todo que
            # e entregue nos dois contratos e multiplica pela energia gerada. A energia gerada sera
            # multiplicada pela quant de horas do mes para que ele fique em KW/h
            eger = (sazonalidadeC1[i]/(sazonalidadeC1[i] +
                    sazonalidadeC2[i]))*(energiaGerada1[i] * horasPmes[i])

            # acima foram definidas as variaveis agora vamos ao calculo
            receitaMes = (precoC1 * econt) + ((eger - econt)*pld[i])
            numeroFormatado = "{:,.3f}".format(receitaMes)
            receitaC1 += receitaMes
            #print(f"A receita do mes {i+1} eh {numeroFormatado}")

        numeroFormatado2 = "{:,.3f}".format(receitaC1)
        print(f"Receita total para o contrato 1: {numeroFormatado2}")
        econt = 0
        eger = 0
        receitaMes = 0

        print("\n")

        # CALCULO DO SEGUNDO CONTRATO
        for i in range(12):
            # energia contratada
            econt = sazonalidadeC2[i] * horasPmes[i]
            # calculo do percentual da energia gerada que pega o proporcional do todo que
            # e entregue nos dois contratos e multiplica pela energia gerada. A energia gerada sera
            # multiplicada pela quant de horas do mes para que ele fique em KW/h
            eger = (sazonalidadeC2[i]/(sazonalidadeC1[i] +
                    sazonalidadeC2[i]))*(energiaGerada1[i] * horasPmes[i])

            # acima foram definidas as variaveis agora vamos ao calculo
            receitaMes = (precoC2 * econt) + ((eger - econt)*pld[i])
            receitaC2 += receitaMes
            numeroFormatado3 = "{:,.3f}".format(receitaMes)
            #print(f"A receita do mes {i+1} eh {numeroFormatado3}")

        numeroFormatado4 = "{:,.3f}".format(receitaC2)
        print(f"Receita total para o contrato 2: {numeroFormatado4}")



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

    calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2, best_solution, precoC1, precoC2, controle, receitaC1, receitaC2)


if __name__ == '__main__':
    genetic_algorithm()
