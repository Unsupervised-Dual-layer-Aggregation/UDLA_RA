import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import os

# Nome do dataset e diretório raiz
dataset_name = "cub200"
root_dir = os.getcwd()

# Caminho do arquivo CSV
csv_path = os.path.join(root_dir, f'{dataset_name}_index.csv')

# Carregar o arquivo CSV
dados = pd.read_csv(csv_path, delimiter=';')

# Ordenar os dados
dados = dados.sort_values(by=['Top K', 'Alpha'])

# Extrair as colunas relevantes
mapa = dados['MAP']
alpha = dados['Alpha']
top_k = dados['Top K']

# Configurar a figura com tamanho maior
# Configurar a figura com tamanho maior e ajustar o layout
fig = plt.figure(figsize=(30, 30))
ax = fig.add_subplot(111, projection='3d')

# Plotar o gráfico de superfície
ax.plot_trisurf(top_k, alpha, mapa, cmap='viridis', edgecolor='none')

# Ajustar os limites dos eixos
ax.set_xlim(min(top_k), max(top_k))
ax.set_ylim(min(alpha), max(alpha))
ax.set_zlim(min(mapa), max(mapa))

# Configurar os rótulos dos eixos com tamanhos de fonte maiores
ax.set_xlabel('Top K', fontsize=35, labelpad=30)
ax.set_ylabel('Alpha', fontsize=35, labelpad=30)
ax.set_zlabel('MAP', fontsize=35, labelpad=30)
ax.zaxis.label.set_rotation(90)

# Posicionar o rótulo do eixo z à esquerda
#ax.zaxis.set_label_coords(-0.1, 0.5)

# Configurar o título do gráfico
ax.set_title(f'Surface Graph', fontsize=18)

# Ajustar as margens para evitar corte do rótulo
plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)

# Aumentar a fonte dos valores dos eixos
ax.tick_params(axis='both', which='major', labelsize=30)
ax.tick_params(axis='z', which='major', labelsize=30)

# Formatar os valores do eixo z com três casas decimais
ax.zaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))

# Ajustar o layout para evitar sobreposição de elementos
plt.tight_layout()

# Salvar o gráfico com alta resolução
plt.savefig(f'{root_dir}/{dataset_name}_surf.png', dpi=300)