import PyCascadeAggreg.pca_calls as pca_calls
import math

# cub200 | oxford17flowers | corel5k
# datasets = {"cub200":60 , "oxford17flowers": 80, "corel5k": 100}
dataset_name = "cub200"
top_k = 100
top_m = 6
alpha = 0.50
#beta = 1
l_size = 3500

#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
agg_method_layer_one = "rdpac"
agg_method_layer_two = "cprr"

# Método a ser considerado na estimativa de eficácia b - borda / a - authority / r - reciprocal
evall_mode = "b"

# Opções de outlayer: Utilizando o arquivo txt de validação ("outlayer_file")/ Considerar apenas redes neurais ("only_nn_descriptors")/ Considerar apenas os descritors classicos ("only_classic_descriptors")
outlayer = "outlayer_file"

# Número de elementos que serão combinados durante a primeira camada de fusão em cada iteração
number_combinations = 2


# Como será considerada a seleção de elementos na fusão da camada dois: "exit_fusions" /considera alpha * os elementos de saida da camada um, "alpha_m" / considera alpha * o valor do top_m da camada um e "m_raw" / consira o mesmop valor de top_m da primeira camada
top_m_lt_type = "exit_fusions" 


# Chamada da execução do código
pca_calls.cascade_execute(dataset_name, top_k, top_m, agg_method_layer_one, agg_method_layer_two, outlayer, evall_mode, alpha, l_size, top_m_lt_type)