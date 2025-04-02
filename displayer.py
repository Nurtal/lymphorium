import matplotlib.pyplot as plt
import glob
import imageio.v2 as imageio
import pandas as pd


def display_logs(log_folder:str, output_file:str) -> None:
    """Display Metrics present in log_folder

    Args:
        - log_folder (str) : path to the log folder
        - output_file (str) : path to save the figure

    """

    # params
    file_to_label = {
        "nb_bcell.csv" : "Bcells (Total)",
        "nb_tcell.csv": "Tcells",
        "nb_activated_bcell.csv": "Activated Bcells",
        "nb_naive_bcell.csv": "Naive Bcells",
        "nb_total.csv": "Total",
    }

    # craft figure
    plt.figure(figsize=(10, 6))
    for file in list(file_to_label.keys()):
        l = file_to_label[file]
        file = f"{log_folder}/{file}"
        df = pd.read_csv(file)
        plt.plot(df["STEP"], df["VALUE"], label=l)
    plt.xlabel("STEP")
    plt.ylabel("VALUE")
    plt.title("Simulation Logs")
    plt.legend()
    plt.grid()
    plt.savefig(output_file)
    plt.close()


def craft_simulation_animation(figure_folder:str, output_file:str) -> None:
    """Use png images in figire folder to craft a gif

    Args:
        - figure_folder (str) : path to the folder with png files
        - output_file (str) : path to the gif file
    
    """
    
    # load & sort images
    files = sorted(glob.glob(f"{figure_folder}/step_*.png"))
    frames = [imageio.imread(img) for img in files]

    # save GIF
    imageio.mimsave(output_file, frames, duration=0.5)

