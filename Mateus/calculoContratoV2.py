import numpy as np

# horas do dia multiplicadas pelos dias do mês
horasPmes = np.array([744.00, 672.00, 744.00, 720.00, 744.00, 720.00,
                     744.00, 744.00, 720.00, 744.00, 720.00, 744.00])  # horas para cada mes
# diasPmes = np.array([31, 28, 31, 30, 31,30,31,31,30,31,30,31]) #dias para cada mes
pld = np.array([242.72, 165.98, 109.02, 132.63, 218.70, 336.99,
               583.88, 583.88, 577.37, 249.36, 88.10, 66.67])  # em R$/MWh

# Energia gerada a cada mês
# energiaGerada1 = np.array([33.83, 34.90, 35.44, 35.11, 38.93, 44.30,47.14, 46.71, 45.64, 43.22, 36.78, 37.58])  # em MWmed_mês
energiaGerada1 = np.array([30.00, 28.00, 25.00, 20.00, 25.00,
                          26.00, 27.00, 30.00, 50.00, 70.00, 65.00, 30.00])  # em MWmed_mê

# como a sazonalidade do contrato 1 é flat, defini para testes que será entregue todo o combainado
sazonalidadeC1 = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
# sazonalidade do segundo contrato
sazonalidadeC2 = np.array([30, 30, 30, 30, 30, 30, 15, 10, 9, 10, 8, 8])

# garantia fisica do parque, que representa a media anual da sazonalizacao total
gfParque = 50
# sazonalidade a cada mês que é o X da nossa questao, esse array não pode ter a media maior que 40
sazonalidadeMes = np.array([50.00, 50.00, 50.00, 50.00, 50.00,
                           50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00])  # MWmed

# DADOS DOS DOIS CONTRATOS
# contrato1
precoC1 = 120
flexibilidadeC1 = 0.3
receitaC1 = 0

# contrato2
precoC2 = 190
flexibilidadeC2 = 0
receitaC2 = 0

receitaTotalSobra = 0

# Controle que realiza a verificacao se a garantia fisica do mes e maior que a soma da energia entregue nos contratos
# se for maior: codigo continua, se for menor: codigo abortado
controle = True


def calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2, sazonalidadeMes, precoC1, precoC2, controle, receitaC1, receitaC2, receitaTotalSobra):

    for i in range(12):
        if (sazonalidadeMes[i] < (sazonalidadeC1[i] + sazonalidadeC2[i])):
            controle = False
            print(
                f"A sonalidade do mes {i+1} eh menor do que a soma da energia entregue nos contratos")

    # variavel para armazenar a receita a cada mes
    receitaMes = 0

    if (controle):
        # CALCULO DO PRIMEIRO CONTRATO
        for i in range(12):
            # energia contratada
            econt = sazonalidadeC1[i] * horasPmes[i]
            # calculo do percentual da energia gerada que pega o proporcional do todo que
            # e entregue nos dois contratos e multiplica pela energia gerada. A energia gerada sera
            # multiplicada pela quant de horas do mes para que ele fique em KW/h
            eger = (sazonalidadeC1[i]/sazonalidadeMes[i]
                    )*(energiaGerada1[i] * horasPmes[i])

            # acima foram definidas as variaveis agora vamos ao calculo
            receitaMes = (precoC1 * econt) + ((eger - econt)*pld[i])
            numeroFormatado = "{:,.3f}".format(receitaMes)
            receitaC1 += receitaMes
            # print(f"A receita do mes {i+1} eh {numeroFormatado}")

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
            eger = (sazonalidadeC2[i]/sazonalidadeMes[i]
                    )*(energiaGerada1[i] * horasPmes[i])

            # acima foram definidas as variaveis agora vamos ao calculo
            receitaMes = (precoC2 * econt) + ((eger - econt)*pld[i])
            receitaC2 += receitaMes
            numeroFormatado3 = "{:,.3f}".format(receitaMes)
            # print(f"A receita do mes {i+1} eh {numeroFormatado3}")

        numeroFormatado4 = "{:,.3f}".format(receitaC2)
        print(f"Receita total para o contrato 2: {numeroFormatado4}")

        for i in range(12):
            # calculo da energia que sobra de acordo com a nova explicação realizada pelo professor

            # calculça o percentual de energia gerada que deve ser empregada em cada um dos contratos
            percentualC1 = sazonalidadeC1[i]/sazonalidadeMes[i]
            percentualC2 = sazonalidadeC2[i]/sazonalidadeMes[i]

            # multiplica a energia gerada total pelo percentual entregue em cada um dos contratos
            egerEntregueC1 = energiaGerada1[i] * percentualC1
            egerEntregueC2 = energiaGerada1[i] * percentualC2
            # calcula o que sobra de energia
            sobraEnergia = energiaGerada1[i] - \
                (egerEntregueC1 + egerEntregueC2)

            # pega a sobra e multiplica pelo valor do PLD e das horas do mês para que gere o retorno de energia vendida
            receitaDaSobra = sobraEnergia * pld[i] * horasPmes[i]
            receitaTotalSobra += receitaDaSobra

            numeroFormatado5 = "{:,.3f}".format(receitaDaSobra)
            # print(f"A receita da sobra do mes {i+1} eh {numeroFormatado5}")

        numeroFormatado6 = "{:,.3f}".format(receitaTotalSobra)
        print(f"Receita total da sobra eh: {numeroFormatado6}")

        receitaTotalEmpresa = receitaC1 + receitaC2 + receitaTotalSobra
        numeroFormatado7 = "{:,.3f}".format(receitaTotalEmpresa)
        print(f"Receita total da empresa eh: {numeroFormatado7}")


calculoContratos(horasPmes, pld, energiaGerada1, sazonalidadeC1, sazonalidadeC2,
                 sazonalidadeMes, precoC1, precoC2, controle, receitaC1, receitaC2, receitaTotalSobra)
