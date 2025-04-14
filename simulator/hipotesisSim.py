import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression

# Parámetros del modelo
num_simulaciones = 1000
tiempo_simulacion = 365  # días
lambda_reclamos = 0.1  # tasa de reclamos por día
media_reclamo = 1000   # monto promedio de reclamo
prima = 150            # ingreso por día

# Simulaciones para diferentes capitales iniciales
capitales_iniciales = np.arange(1000, 20000, 1000)
resultados_ruina = []

def simular_ruina(capital_inicial):
    for _ in range(num_simulaciones):
        capital = capital_inicial
        for t in range(tiempo_simulacion):
            ingresos = prima
            num_reclamos = np.random.poisson(lambda_reclamos)
            monto_total = np.sum(np.random.exponential(media_reclamo, size=num_reclamos))
            capital += ingresos - monto_total
            if capital < 0:
                return 1  # ruina
        return 0  # no hubo ruina

# Ejecutar simulaciones
for a0 in capitales_iniciales:
    ruinas = [simular_ruina(a0) for _ in range(num_simulaciones)]
    probabilidad_ruina = np.mean(ruinas)
    resultados_ruina.append((a0, probabilidad_ruina))

# Separar datos
X = np.array([r[0] for r in resultados_ruina]).reshape(-1, 1)
y = np.array([int(p > 0.05) for _, p in resultados_ruina])  # 1 si hay riesgo significativo de ruina

# Regresión logística
X_const = sm.add_constant(X)
modelo_logit = sm.Logit(y, X_const).fit()

print(modelo_logit.summary())

# Visualización
capitales = X.flatten()
probabilidades_ruina = [r[1] for r in resultados_ruina]

plt.figure(figsize=(8, 5))
plt.plot(capitales, probabilidades_ruina, marker='o', linestyle='-')
plt.xlabel("Capital inicial $a_0$")
plt.ylabel("Probabilidad estimada de ruina")
plt.title("Probabilidad de ruina vs capital inicial")
plt.grid(True)
plt.tight_layout()
plt.savefig("probabilidad_ruina_vs_capital.png")
plt.show()
