import pandas as pd
import numpy as np

np.random.seed(42)
n = 500

#  dados utilizados são simulados para representar cenários reais de auditoria, incluindo inconsistências intencionais para análise.

df = pd.DataFrame({
    'data': pd.date_range('2024-01-01', periods=n, freq='D').to_list()[:n],
    'funcionario': np.random.choice(['Ana Silva','Carlos Matos','Beatriz Lima','João Costa'], n),
    'departamento': np.random.choice(['TI','Comercial','RH','Financeiro'], n),
    'categoria': np.random.choice(['Viagem','Alimentação','Software','Treinamento','Outros'], n),
    'valor': np.abs(np.random.normal(850, 600, n)).round(2),
    'aprovado': np.random.choice([True, False], n, p=[0.85, 0.15])
})

# Insert abnormal value (audit simulation)
df.loc[10, 'valor'] = 28500.00   
df.loc[77, 'valor'] = 15300.00
df.loc[200, 'aprovado'] = False   
df.to_csv('despesas.csv', index=False)
print(df.head())

# 1. Employee-Based Analysis
resumo = df.groupby('departamento')['valor'].agg(['mean','sum','count','max'])
print(resumo)

# 2. Outlier Detection (IQR Method)
Q1 = df['valor'].quantile(0.25)
Q3 = df['valor'].quantile(0.75)
IQR = Q3 - Q1
alertas = df[df['valor'] > Q3 + 1.5 * IQR]
print(alertas)

# 3. Payments not approved
nao_aprovados = df[df['aprovado'] == False]
print(nao_aprovados)

# 4. Identify highest volume
top_gastos = df.groupby('funcionario')['valor'].sum().sort_values(ascending=False)
print(top_gastos)
