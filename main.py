import tetris
import numpy as np
import itertools

population_size = 200
no_of_features = 4
selection_portion = 0.5 #percentage of population to keep every round
    
def ga_main():

    no_of_iterations = 25

    #generate initial solution
    solns_weight_arr = np.random.randn(population_size, no_of_features) * 10
    
    for i in range(no_of_iterations):
        print "iteration %s ans:" %(i)        
        solns_weight_arr = ga_train_once(solns_weight_arr)
        # print solns_weight_arr
    
def ga_train_once(solns_weight_arr):
    
    #run and get back an array of results
    results_list = []
    for weight_arr in solns_weight_arr:
        results_list.append( simulate_for_results(weight_arr) )
    results_list = np.array(results_list)

    #population undergo selection 
    results_rank_list = np.argsort(results_list)
    selected_list = results_rank_list[(population_size/2):]
    #selected_list=results_rank_list[results_rank_list > int(population_size*selection_portion)]
    #selected_weights_arr = solns_weight_arr[selected_list]
        
    #selected population undergo crossover
    possible_combinations = list(itertools.combinations(selected_list, 2))
    selected_combinations = np.random.choice(len(possible_combinations), population_size)
    
    new_pool = []    
    for combination in selected_combinations:
        first_layer = np.random.choice(2,4)
        second_layer = np.fmod(first_layer+1, 2)
        comb_weight_arr = solns_weight_arr[possible_combinations[combination][0]] * first_layer + solns_weight_arr[possible_combinations[combination][1]] * second_layer
        new_pool.append(comb_weight_arr)
        
    #selected population undergo mutation
    for gene in new_pool:
        #10% chance of mutating every gene        
        if np.random.uniform(0,1,1) < 0.1:
            #print "mutating: %s" %(gene)
            #print gene
            #mutate one of its features
            feature_to_mutate = np.random.randint(0,4)
            gene[feature_to_mutate] = np.random.randn(1) * 10
            #print "mutated: %s" %(gene)
    return new_pool
    
def simulate_for_results(wt_arr):
    try:
        #run the game and get back the result
        app = tetris.TetrisApp(wt_arr, True)
        app.run()
        print(app.score)
    except ValueError: 
        print("Error")
        print(app.board)
        print(app.block.value)
        print(app.block.x)
        print(app.block.y)

    #appends to file
    with open("output.txt", "a") as f:
        f.write("{},{}\n".format(app.score, ",".join(wt_arr.astype(str))))

    return app.score
    #return result_arr

ga_main()