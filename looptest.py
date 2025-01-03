import PyCascadeAggreg.pca_calls as pca_calls
import PyCascadeAggreg.pca_plotlib as plot
from decimal import Decimal

# cub200 | oxford17flowers | corel5k
# datasets = {"cub200":3500 , "oxford17flowers": 1360, "corel5k": 3500}
datasets = ["corel5k"]
evall_mode = "b"
outlayer = "outlayer_file"
top_m_lt_type = "exit_fusions"
end_range = 1.0
l_size = 3500
#alpha = Decimal("0.5")
#beta = 1.0
#top_k = 50
#NONE|CPRR|RLRECOM|RLSIM|CONTEXTRR|RECKNNGRAPH|RKGRAPH|CORGRAPH|LHRR|BFSTREE|RDPAC|RFE
agg_methods_layer_one = ["rdpac"]
agg_methods_layer_two = ["cprr"]
for dataset_name in datasets:
    for agg_method_layer_one in agg_methods_layer_one:
        for agg_method_layer_two in agg_methods_layer_two:
            for top_m in range(1, 6, 1):
                for top_k in range(50, 101, 25):
                    if top_m == 3:  
                        alpha = Decimal("0.50")
                    else:
                        alpha = Decimal("0.25")
                    while alpha <= end_range:
                        # Chamada da execução do código
                        pca_calls.cascade_execute(dataset_name, top_k, top_m, agg_method_layer_one, agg_method_layer_two, outlayer, evall_mode, alpha,l_size, top_m_lt_type)
                        alpha = alpha + Decimal("0.25")
    
    plot.plot_surf_graph(dataset_name)