from cluster_mlp.deap_main import cluster_GA
from ase.data import atomic_numbers, atomic_names, atomic_masses, covalent_radii
from ase.calculators.emt import EMT
from ase.visualize import view

eleNames = ['Cu', 'Al']
eleNums = [3, 5]
nPool = 10
generations = 40
CXPB = 0.4
eleRadii = [covalent_radii[atomic_numbers[ele]] for ele in eleNames]
filename = 'cluster_GA_test' #For saving the best cluster at every generation
calc = EMT()

bi,final_cluster = cluster_GA(nPool,eleNames,eleNums,eleRadii,generations,calc,filename,CXPB)
view(final_cluster)
view(bi[0])
