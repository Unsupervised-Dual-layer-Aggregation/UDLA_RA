import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_dot_graph(output_dataset_path: str, dataset_name: str, best_map_fusion: float, top_m: int):
    root_dir = os.getcwd()

    try:
        # Carrega os dados do CSV de descritores isolados
        descriptors_dataset = pd.read_csv(f"{output_dataset_path}/{dataset_name}.csv", delimiter=";")
    except FileNotFoundError:
        print(f"Não foi possível localizar o arquivo {dataset_name}.csv")
        return
    
    try:
        # Carrega os dados do CSV de descritores isolados
        fusion_values = pd.read_csv(f"{output_dataset_path}/{dataset_name}_cascade.csv", delimiter=";")
    except FileNotFoundError:
        print(f"Não foi possível localizar o arquivo {dataset_name}_cascade.csv")
        return
    
    # Encontrando o maior valor da coluna "MAP" no arquivo de descritores isolados
    best_MAP = descriptors_dataset["MAP"].max()

    # Lê os campos "descriptor" e "borda score" do dataframe e em seguida ordena pela coluna "borda score" em ordem crescente
    borda_values = fusion_values[["descriptor", "borda score"]].sort_values(by="borda score", ascending=True)

    # Criando uma lista vazia para armazenar as cores
    colors = []  

    # Adicionando o valor do ponto e definindo a cor
    for i in range(len(borda_values)):
        if fusion_values.loc[fusion_values['descriptor'] == borda_values.iloc[i]["descriptor"], "MAP"].values[0] >= best_MAP:
            # Adicionando 'green' para valores maiores que best_MAP
            colors.append('green')  
        else:
            # Adicionando 'blue' para valores menores que best_MAP
            colors.append('blue')  

    # Crie rótulos personalizados com números e descritores
    enumerated_elements = [f"{i+1}. {txt}" for i, txt in enumerate(borda_values["descriptor"])]

    plt.figure(figsize=(15, 15))  # Dimensões quadradas da figura
    
    plt.rc('font', size=40)

    # Gráfico principal
    plt.scatter(borda_values["borda score"], [fusion_values.loc[fusion_values['descriptor'] == desc, "MAP"].values[0] for desc in borda_values["descriptor"]], c=colors)
    best_isolate_line = plt.axhline(y=best_MAP, color='red', linestyle='--', label="Best Isolate Ranker")
    second_layer_line = plt.axhline(y=best_map_fusion, color='blue', linestyle="dashdot", label="Second Layer Fusion")
    
    # Adicionando a legenda das linhas
    plt.legend(handles=[best_isolate_line, second_layer_line], loc='best')

    plt.xlabel("Borda Rank", fontsize=24)
    plt.ylabel("MAP", fontsize=24)
    plt.title("Pairwise Rankers Fusion")
    plt.grid(True)

    plt.tick_params(axis='x', labelsize=25)
    plt.tick_params(axis='y', labelsize=25)

    # Adicionando os números aos pontos no gráfico
    for i, txt in enumerate(enumerated_elements):
        plt.annotate(i+1, (borda_values["borda score"].iloc[i], fusion_values.loc[fusion_values['descriptor'] == borda_values["descriptor"].iloc[i], "MAP"].values[0]), textcoords="offset points", xytext=(5,5), ha='center')

    plt.tight_layout()
    plotname = output_dataset_path.split("/")[-1]

    # Salvar como PDF em alta resolução
    plt.savefig(f'{root_dir}/{dataset_name}_graph.pdf', format='pdf', dpi=300)
    plt.show()

    return



root_dir = os.getcwd()
id_exec = "b3614134-77d5-4cf6-ae26-85a246d1f525"
dataset_name = "corel5k"
output_dataset_path = f"{root_dir}/output/{dataset_name}/{id_exec}"
top_m = 6
best_map_fusion = 0.9751
plot_dot_graph(output_dataset_path, dataset_name, best_map_fusion, top_m)
