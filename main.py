from simulator.simulation import (
    estimate_survival_probability,
    simulate_insurance_run,
)
from simulator.visualizations import (
    plot_capital_evolution,
    save_results
)

# Estimación de probabilidad de supervivencia
prob, results = estimate_survival_probability(runs=1000)
print(f"Probabilidad estimada de NO ruina: {prob:.4f}")
save_results(results)

# Graficar una simulación de ejemplo
T = 100  # Tiempo total de simulación
a_0 = 1000  # Capital inicial
n_0 = 10  # Número inicial de asegurados
c = 10  # Ingreso por prima por cliente por unidad de tiempo
lam = 0.1  # Tasa de reclamos por cliente
mu = 0.05  # Tasa de abandono de clientes
nu = 0.2  # Tasa de llegada de nuevos clientes

# Ejecutar una simulación
t, a, _ = simulate_insurance_run(T, a_0, n_0, c, lam, mu, nu)

# Graficar la evolución del capital
plot_capital_evolution(t, a)
