# Valores de entrada
Preco_Contrato = 155
Valor_Contratado_Mes = 30
Valor_Contratado_Max_Mensal = 70
Total_Energia_Gerada = 63240
PLD = 256
Numero_Horas_Mes = 31 * 24

# Calculando a energia consumida
Energ_Consumida = (Valor_Contratado_Mes / Valor_Contratado_Max_Mensal) * Total_Energia_Gerada

# Calculando a energia contratada
Energ_Contratada = Valor_Contratado_Mes * Numero_Horas_Mes

# Calculando a receita
Receita = (Preco_Contrato * Valor_Contratado_Mes * Numero_Horas_Mes) + (((Energ_Consumida - Energ_Contratada) * PLD))

print("Receita total:", Receita)
