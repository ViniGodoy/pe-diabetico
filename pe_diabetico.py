import pandas as pd
import statistics
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
import numpy as np

gabarito = {
    "q1-1": "s", "q1-2": "s", "q1-3": "n", "q1-4": "s",
    "q2-1": "n", "q2-2": "n", "q2-3": "n", "q2-4": "s",
    "q3-1": "n", "q3-2": "s", "q3-3": "n", "q3-4": "n",
    "q4-1": "n", "q4-2": "n", "q4-3": "n", "q4-4": "x",
    "q5-1": "s", "q5-2": "n", "q5-3": "n", "q5-4": "n",
    "q6-1": "s", "q6-2": "n", "q6-3": "n", "q6-4": "s",
    "q7-1": "s", "q7-2": "s", "q7-3": "s", "q7-4": "s",
    "q9-1": "n", "q9-2": "n", "q9-3": "s", "q9-4": "n",
    "q10-1": "x", "q10-2": "n", "q10-3": "n",
    "q11-1": "n", "q11-2": "n", "q11-3": "s", "q11-4": "n",
    "q12-1": "2-3 meses",
    "q13-1": "sim",
    "q15-1": "sim",
    "q16-1": "frequente", "q16-2": "frequente", "q16-3": "frequente", "q16-4": "frequente",
    "q16-5": "frequente", "q16-6": "frequente", "q16-7": "frequente", "q16-8": "frequente",
    "q16-9": "frequente", "q16-10": "frequente", "q16-11": "frequente", "q16-12": "frequente",
    "q16-13": "frequente", "q16-15": "frequente", "q16-16": "frequente",
    "q16-17": "pouco frequente", "q16-18": "frequente", "q16-19": "pouco frequente",
    "q17-1": "anualmente", "q17-2": "3-6 meses", "q17-3": "2-3 meses", "q17-4": "3-6 meses",
    "q17-5": "2-3 meses", "q17-6": "1-2 meses", "q17-7": "1-2 meses",
}


def chave_sort(k):
    partes = k.replace("q", "").split("-")
    return int(partes[0]), int(partes[1])


chaves_ordenadas = sorted(gabarito.keys(), key=chave_sort)

df = pd.read_csv("respostas.csv")

acertos_antes = []
acertos_depois = []

for _, linha in df.iterrows():
    if pd.isna(linha['numero']):
        continue

    num = str(int(linha['numero']))
    antes = []
    depois = []

    for q in chaves_ordenadas:
        col_a = f"{q}-a"
        col_d = f"{q}-d"

        ans_a = str(linha[col_a]).strip().lower() if col_a in df.columns else ""
        ans_d = str(linha[col_d]).strip().lower() if col_d in df.columns else ""
        gab = gabarito[q].strip().lower()

        antes.append(1 if ans_a == gab else 0)
        depois.append(1 if ans_d == gab else 0)

    acertos_antes.append(sum(antes))
    acertos_depois.append(sum(depois))

    print(f'"{num}": {{\n   "antes": {antes},\n   "depois": {depois}\n}}')

# Cálculo da diferença absoluta
diferenca = [d - a for a, d in zip(acertos_antes, acertos_depois)]

print(f"{'antes':>9}: [{', '.join(f'{x:>2}' for x in acertos_antes)}]")
print(f"{'depois':>9}: [{', '.join(f'{x:>2}' for x in acertos_depois)}]")
print(f"{'diferenca':>9}: [{', '.join(f'{x:>2}' for x in diferenca)}]")

# Teste de Wilcoxon
stat, p = wilcoxon(acertos_antes, acertos_depois)
print(f"\n--- TESTE DE WILCOXON ---")
print(f"Estatística: {stat}")
print(f"p-value: {p:.4f}")

# Estatísticas Descritivas
print(f"\n--- COMPARATIVO DE NOTAS ---")
print(f"Média Antes:   {statistics.mean(acertos_antes):.2f}")
print(f"Média Depois:  {statistics.mean(acertos_depois):.2f}")
print(f"Mediana Antes:  {statistics.median(acertos_antes):.2f}")
print(f"Mediana Depois: {statistics.median(acertos_depois):.2f}")
print(f"Desvio Padrão Antes:  {statistics.stdev(acertos_antes):.2f}")
print(f"Desvio Padrão Depois: {statistics.stdev(acertos_depois):.2f}")

alunos = np.arange(1, len(acertos_antes) + 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Plot Antes
mean_a = np.mean(acertos_antes)
std_a = np.std(acertos_antes, ddof=1)
ax1.scatter(alunos, acertos_antes, color='#1f77b4', s=100, edgecolor='black', zorder=3)
ax1.axhline(mean_a, color='red', linestyle='--', label=f'Média: {mean_a:.1f}')
ax1.fill_between([0, 15], mean_a - std_a, mean_a + std_a, color='red', alpha=0.1, label=f'Desvio Padrão: ±{std_a:.1f}')
ax1.set_title('Antes da Intervenção')
ax1.set_xlabel('Questionário')
ax1.set_ylabel('Total de Acertos')
ax1.set_xlim(0.5, 14.5)
ax1.set_ylim(15, 55) # Fixa os limites para ambos os gráficos
ax1.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax1.legend(loc='upper left')

# Plot Depois
mean_d = np.mean(acertos_depois)
std_d = np.std(acertos_depois, ddof=1)
ax2.scatter(alunos, acertos_depois, color='#2ca02c', s=100, edgecolor='black', zorder=3)
ax2.axhline(mean_d, color='red', linestyle='--', label=f'Média: {mean_d:.1f}')
ax2.fill_between([0, 15], mean_d - std_d, mean_d + std_d, color='red', alpha=0.1, label=f'Desvio Padrão: ±{std_d:.1f}')
ax2.set_title('Depois da Intervenção')
ax2.set_xlabel('Questionário')
ax2.set_xlim(0.5, 14.5)
ax2.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax2.legend(loc='upper left')

plt.tight_layout()
plt.savefig('dispersao_lado_a_lado.png', bbox_inches='tight')

questao8 = {
    "pre": [2, 0, 1, 1, 0, 2, 4, 0, 2, 0, 0, 0, 0, 1],
    "pos": [4, 1, 5, 5, 1, 5, 1, 2, 2, 1, 5, 0, 0, 1]
}
stat8, p8 = wilcoxon(questao8["pre"], questao8["pos"])
print(f"\n--- TESTE DE WILCOXON QUESTAO 8 ---")
print(f"Estatística: {stat8}")
print(f"p-value: {p8:.4f}")
print(f"Mediana antes: {statistics.median(questao8["pre"]):.2f}")
print(f"Mediana depois: {statistics.median(questao8["pos"]):.2f}")
print(f"Media antes: {statistics.mean(questao8["pre"]):.2f}")
print(f"Media depois: {statistics.mean(questao8["pos"]):.2f}")
print(f"Desvio Padrão Antes:  {statistics.stdev(questao8["pre"]):.2f}")
print(f"Desvio Padrão Depois: {statistics.stdev(questao8["pos"]):.2f}")

# 2. Preparação dos dados para o gráfico
antes = questao8["pre"]
depois = questao8["pos"]
alunos = np.arange(1, len(antes) + 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# --- Plot Antes ---
mean_a = np.mean(antes)
std_a = np.std(antes, ddof=1)

ax1.scatter(alunos, antes, color='#1f77b4', s=100, edgecolor='black', zorder=3)
ax1.axhline(mean_a, color='red', linestyle='--', label=f'Média: {mean_a:.1f}')
ax1.fill_between([0, 15], mean_a - std_a, mean_a + std_a, color='red', alpha=0.1, label=f'Desvio Padrão: ±{std_a:.1f}')

ax1.set_title('Antes da intervenção')
ax1.set_xlabel('Questionário')
ax1.set_ylabel('Total de acertos')
ax1.set_xlim(0.5, 14.5)

# Normalização do eixo Y para abranger os limites de ambos os arrays
max_y = max(max(antes), max(depois)) + 1
min_y = min(min(antes), min(depois)) - 1
ax1.set_ylim(min_y, max_y)
ax1.set_yticks(np.arange(0, max_y, 1))

ax1.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax1.legend(loc='upper left')


# --- Plot Depois ---
mean_d = np.mean(depois)
std_d = np.std(depois, ddof=1)

ax2.scatter(alunos, depois, color='#2ca02c', s=100, edgecolor='black', zorder=3)
ax2.axhline(mean_d, color='red', linestyle='--', label=f'Média: {mean_d:.1f}')
ax2.fill_between([0, 15], mean_d - std_d, mean_d + std_d, color='red', alpha=0.1, label=f'Desvio Padrão: ±{std_d:.1f}')

ax2.set_title('Depois da Intervenção')
ax2.set_xlabel('Questionário')
ax2.set_xlim(0.5, 14.5)

ax2.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax2.legend(loc='upper left')

# Renderização final
plt.tight_layout()
plt.savefig('dispersao_questao8.png', bbox_inches='tight')