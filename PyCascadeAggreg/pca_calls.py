import os, time, shutil, atexit
import PyCascadeAggreg.pca_utils as utils
import PyCascadeAggreg.pca_effectiveness as effectiv
import PyCascadeAggreg.pca_savefiles as savefile
import PyCascadeAggreg.pca_aggregate as aggregate
import PyCascadeAggreg.pca_rk_compute as rkc
import PyCascadeAggreg.pca_plotlib as plotlib
from datetime import datetime


def cascade_execute(dataset_name: str,top_k: int, top_m: int, agg_method_layer_one: str, agg_method_layer_two: str, outlayer: str, evall_mode: str, alpha: float, l_size: int, top_m_lt_type: str, number_combinations = 2):
    

    def rm_path(path_way:str):
        
        path_sel = path_way.split("/")[-1]

        try:
            print(f"Iniciando limpeza de listas na pasta {path_sel}")
            shutil.rmtree(path_way)
            print("Limpeza concluída! \n")
        except:
            print(f"Falha na limpeza do caminho informado!: {path_way}")
        return
    
    # Obtém a data e hora atuais
    date_raw = datetime.now()
    # Formata a data e hora no formato desejado
    date_formated = date_raw.strftime("%d/%m/%y %H:%M:%S")

    initial_time = time.time()

    # Valida o valor minimo do top M, calcula o tamanho da saida da cascata e valida o modo de estimativa de eficácia
    # cascade_size: int -> Número de elementos resultante da combinações da cascata
    # evall_mode: str
    cascade_size, evall_mode = utils.validate_data(top_m, number_combinations, evall_mode)
    
    # rootDir: str -> Pasta raiz do código
    rootDir = os.getcwd()

    # dataset-path: Str -> Caminho para pasta do dataset
    dataset_path = f"{rootDir}/dataset/{dataset_name}"

    # Cria as pastas caso necessário e armazena os caminhos nas varíaveis 
    output_dataset_path, output_rk_fusion_path, output_rankedlists, csv_index_file, agg_index = utils.paths_creations(
        dataset_name, evall_mode)


    lists_file_path, classes_file_path = utils.get_lists_and_classes_txt(dataset_path)

    dataset_size = utils.get_dataset_size(lists_file_path)
    #l_size = l_size = int(dataset_size * beta)


    if len(os.listdir(output_rankedlists)) != len(os.listdir(f"{rootDir}/dataset/{dataset_name}/features")):
        print("Calculando listas ranqueadas dos descritores isolados")
        rkc.compute_rklists_from_feat(dataset_name, l_size)

    print("\nCalculando valores do MAP, Precision e Recall...")

    utils.get_all_eval(dataset_path, output_dataset_path, outlayer, l_size)

    authority, reciprocal = effectiv.call_compute_descriptors_effectiveness(top_k, f"{dataset_path}/ranked_lists", outlayer) 

    print("\nSalvando os dados das estimativas authority e reciprocal dos descritores isolados...")

    savefile.save_effectiveness_scores(dataset_name, authority, reciprocal, output_dataset_path)

    utils.get_borda_ranked_lists(dataset_name, output_dataset_path)

    aggregate.first_layer_fusion(agg_method_layer_one, dataset_path, evall_mode, top_m, output_dataset_path, output_rk_fusion_path,lists_file_path, classes_file_path, l_size, top_k)

    authority, reciprocal = effectiv.call_compute_descriptors_effectiveness(top_k, output_rk_fusion_path, outlayer)

    print("\nSalvando os dados das estimativas authority e reciprocal dos pares combinados...")

    savefile.save_effectiveness_scores(f"{dataset_name}_cascade", authority, reciprocal, output_dataset_path)

    utils.get_borda_ranked_lists(f"{dataset_name}_cascade", output_dataset_path)

    map_result, top_m_lt = aggregate.second_layer_fusion(agg_method_layer_two, dataset_path, evall_mode, output_dataset_path, output_rk_fusion_path, alpha, lists_file_path, classes_file_path,agg_method_layer_one, top_m, l_size, top_m_lt_type, top_k)

    final_time = time.time()
    run_time = final_time - initial_time

    savefile.save_index(date_formated,csv_index_file, agg_index, dataset_name, agg_method_layer_one, agg_method_layer_two, outlayer, top_k, top_m, top_m_lt_type, top_m_lt, alpha, evall_mode, l_size, map_result,run_time)
    
    plotlib.plot_dot_graph(output_dataset_path, dataset_name, top_k, top_m)
    
        
    print("Iniciando limpeza de dados...")

    if os.path.exists(output_rankedlists):
        rm_path(output_rankedlists)

    if os.path.exists(output_rk_fusion_path):
        rm_path(output_rk_fusion_path)
    
    return