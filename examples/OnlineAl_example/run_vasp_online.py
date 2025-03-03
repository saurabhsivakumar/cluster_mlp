from cluster_mlp.deap_ga import cluster_GA
from ase.data import atomic_numbers, covalent_radii
from ase.calculators.vasp import Vasp
from dask_kubernetes import KubeCluster
from dask.distributed import Client
import torch
from ase.optimize import BFGS
#from ase.optimize import GPMin
from vasp_interactive import VaspInteractive

if __name__ == "__main__":
    use_dask = True
    eleNames = ["Ni"]
    eleNums = [10]
    nPool = 10
    generations = 20
    CXPB = 0.5
    eleRadii = [covalent_radii[atomic_numbers[ele]] for ele in eleNames]
    filename = "clus_Ni10"  # For saving the best cluster at every generation
    log_file = "clus_Ni10.log"
    singleTypeCluster = True
    # calc = EMT()
    calc = Vasp(
        kpar=1,
        ncore=4,
        encut=400,
        xc="PBE",
        kpts=(1, 1, 1),
        gamma=True,  # Gamma-centered
        ismear=1,
        sigma=0.2,
        ibrion=-1,
        nsw=0,
        #potim=0.2,
        isif=0,
        # ediffg=-0.02,
        # ediff=1e-6,
        lcharg=False,
        lwave=False,
        lreal=False,
        ispin=2,
        isym=0,
    )
    use_vasp = True
    use_vasp_inter = False
    al_method = "Online"
    optimizer = BFGS
    if use_dask == True:
        # Run between 0 and 4 1-core/1-gpu workers on the kube cluster
        cluster = KubeCluster.from_yaml("worker-cpu-spec.yml")
        client = Client(cluster)
        # cluster.adapt(minimum=0, maximum=10)
        cluster.scale(10)

    learner_params = {
        "filename": "relax_example",
        "file_dir": "./",
        "stat_uncertain_tol": 0.08,
        "dyn_uncertain_tol": 0.1,
        "fmax_verify_threshold": 0.05,  # eV/AA
    }
    train_config  = {
        "sigma": 4.5,
        "power": 2,
        "cutoff_function": "quadratic",
        "cutoff": 5.0,
        "radial_basis": "chebyshev",
        "cutoff_hyps": [],
        "sigma_e": 0.009,
        "sigma_f": 0.005,
        "sigma_s": 0.0006,
        "hpo_max_iterations": 50,
        "freeze_hyps": 0,
    }


    bi, final_cluster = cluster_GA(
        nPool,
        eleNames,
        eleNums,
        eleRadii,
        generations,
        calc,
        filename,
        log_file,
        CXPB,
        singleTypeCluster,
        use_dask,
        use_vasp,
        al_method,
        learner_params,
        train_config,
        optimizer,
        use_vasp_inter,
    )
