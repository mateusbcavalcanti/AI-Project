import numpy as np

#horas do dia multiplicadas pelos dias do mês
horasPmes = np.array([744.00, 672.00, 744.00, 720.00, 744.00, 720.00, 744.00, 744.00, 720.00, 744.00, 720.00, 744.00])#horas para cada mes
#diasPmes = np.array([31, 28, 31, 30, 31,30,31,31,30,31,30,31]) #dias para cada mes
pld = np.array([242.72, 165.98, 109.02, 132.63, 218.70, 336.99, 583.88, 583.88, 577.37, 249.36, 88.10, 66.67]) # em R$/MWh

#Energia gerada a cada mês
energiaGerada1 = np.array([33.83, 34.90, 35.44, 35.11, 38.93, 44.30, 47.14, 46.71, 45.64, 43.22, 36.78, 37.58]) # em MWmed_mês
#energiaGerada2 = np.array([30.00, 28.00, 25.00, 20.00, 25.00, 26.00, 27.00, 30.00, 50.00, 70.00, 65.00, 30.00]) # em MWmed_mê

#como a sazonalidade do contrato 1 é flat, defini para testes que será entregue todo o combainado
sazonalidadeC1 =  np.array([10, 10, 10, 10, 10 ,10, 10, 10, 10, 10, 10, 10])
#sazonalidade do segundo contrato
sazonalidadeC2 =  np.array([30, 30, 30, 30, 30 ,30, 15, 10, 9, 10, 8, 8])

#garantia fisica do parque, que representa a media anual da sazonalizacao total
gfParque = 40
#sazonalidade a cada mês que é o X da nossa questao, esse array não pode ter a media maior que 40
sazonalidadeMes = np.array([40.00, 40.00 ,40.00, 40.00 ,40.00, 40.00 ,40.00, 40.00, 40.00 ,40.00 ,40.00, 40.00]) # MWmed

#DADOS DOS DOIS CONTRATOS
#contrato1
precoC1 = 120
flexibilidadeC1 = 0.3
receitaC1 = 0

#contrato2
precoC2 = 190
flexibilidadeC2 = 0
receitaC2 = 0

#CALCULO DO PRIMEIRO CONTRATO
for i in range(12):
    #energia contratada
    econt = sazonalidadeC1[i] * horasPmes[i]
    # calculo do percentual da energia gerada que pega o proporcional do todo que
    #e entregue nos dois contratos e multiplica pela energia gerada. A energia gerada sera
    #multiplicada pela quant de horas do mes para que ele fique em KW/h 
    eger = (sazonalidadeC1[i]/(sazonalidadeC1[i] + sazonalidadeC2[i]))*(energiaGerada1[i] * horasPmes[i])

    #acima foram definidas as variaveis agora vamos ao calculo
    #se e energia gerada for menor do que o que deve ser entregue nos dois contratos, o excedente será comprado no valor de 110
    if((sazonalidadeC1[i] + sazonalidadeC2[i]) > energiaGerada1[i]):
        receitaC1 = (precoC1 * econt) + ((eger - econt)*110)
        receitaC1 += receitaC1
        print(receitaC1)
    
    #por outro lado, se for maior ou igual, o valor do calculo será o do pld
    else:
        receitaC1 = (precoC1 * econt) + ((eger - econt)*pld[i])
        receitaC1 += receitaC1
        print(receitaC1)

#print(receitaC1)
econt = 0
eger = 0


#CALCULO DO SEGUNDO CONTRATO
for i in range(11):
    #energia contratada
    econt = sazonalidadeC2[i] * horasPmes[i]
    # calculo do percentual da energia gerada que pega o proporcional do todo que
    #e entregue nos dois contratos e multiplica pela energia gerada. A energia gerada sera
    #multiplicada pela quant de horas do mes para que ele fique em KW/h 
    eger = (sazonalidadeC2[i]/(sazonalidadeC1[i] + sazonalidadeC2[i]))*(energiaGerada1[i] * horasPmes[i])

    #acima foram definidas as variaveis agora vamos ao calculo
    #se e energia gerada for menor do que o que deve ser entregue nos dois contratos, o excedente será comprado no valor de 110
    if((sazonalidadeC1[i] + sazonalidadeC2[i]) > energiaGerada1[i]):
        receitaC2 = (precoC2 * econt) + ((eger - econt)*110)
        receitaC2 += receitaC2
        #print(receitaC1)
    
    #por outro lado, se for maior ou igual, o valor do calculo será o do pld
    else:
        receitaC2 = (precoC2 * econt) + ((eger - econt)*pld[i])
        receitaC2 += receitaC2
        #print(receitaC1)

print(receitaC2)