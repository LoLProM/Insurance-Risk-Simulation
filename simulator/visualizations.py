import pandas as pd
import os
import matplotlib.pyplot as plt

def save_results(results, filename="data/results.csv"):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame({"run": list(range(1, len(results)+1)), "no_ruin": results})
    df.to_csv(filename, index=False)


def plot_capital_evolution(times, capitals, filename="figures/capital_evolution.png"):
    os.makedirs("figures", exist_ok=True)
    plt.figure(figsize=(10, 5))
    plt.plot(times, capitals, label="Capital", color="blue")
    plt.axhline(0, color="red", linestyle="--", label="Umbral de ruina")
    plt.xlabel("Tiempo")
    plt.ylabel("Capital")
    plt.title("Evolución del capital de la aseguradora")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()