import numpy as np

def simulate_insurance_run(
    T,           # Tiempo total de simulación
    a_0,         # Capital inicial
    n_0,         # Número inicial de asegurados
    c,           # Ingreso por prima por cliente por unidad de tiempo
    lam,         # Tasa de reclamos por cliente
    mu,          # Tasa de abandono de clientes
    nu,          # Tasa de llegada de nuevos clientes
    claim_dist= None  # Función generadora de reclamos
):
    # Variables del sistema
    t = 0
    a = a_0
    n = n_0
    times = [t]
    capitals = [a]

    # Distribución de reclamos (por defecto: exponencial media 100)
    if claim_dist is None:
        claim_dist = lambda: np.random.exponential(100)

    while True:
        if n == 0:
            rate = nu
        else:
            rate = nu + n * mu + n * lam

        X = np.random.exponential(1 / rate)
        tE = t + X

        if tE > T:
            break

        a += n * c * (tE - t)
        t = tE

        probs = [nu, n * mu, n * lam]
        probs = np.array(probs) / sum(probs)
        J = np.random.choice([1, 2, 3], p=probs)

        if J == 1:
            n += 1
            # Nueva llegada de cliente
        elif J == 2:
            # Abandono de cliente
            n -= 1
        elif J == 3:
            # Reclamo de cliente
            y = claim_dist()
            if y > a:
                return times, capitals, False  # Ruin occurred
            else:
                a -= y

        times.append(t)
        capitals.append(a)

    return times, capitals, True

def estimate_survival_probability(
    runs=1000,
    T_range=(50, 200),
    a_0_range=(1000, 5000),
    n_0_range=(10, 50),
    c_range=(10, 50),
    lam_range=(0.01, 0.5),
    mu_range=(0.01, 0.3),
    nu_range=(0.01, 0.4),
    claim_dist=None
):
    results = []
    for _ in range(runs):
        T = np.random.uniform(*T_range)
        a_0 = np.random.uniform(*a_0_range)
        n_0 = np.random.randint(*n_0_range)
        c = np.random.uniform(*c_range)
        lam = np.random.uniform(*lam_range)
        mu = np.random.uniform(*mu_range)
        nu = np.random.uniform(*nu_range)

        outcome = simulate_insurance_run(
            T=T,
            a_0=a_0,
            n_0=n_0,
            c=c,
            lam=lam,
            mu=mu,
            nu=nu,
            claim_dist=claim_dist
        )
        results.append(outcome[-1])  # Append True/False for survival

    survival_prob = sum(results) / len(results)
    return survival_prob, results
