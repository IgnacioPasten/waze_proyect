import time
import random
import numpy as np

CIUDADES_POPULARES = ["Santiago", "Providencia", "Las Condes", "Maipú", "Ñuñoa"]


class TrafficGenerator:
    def __init__(self, model="uniform", rate=1):
        self.model = model
        self.rate = rate

    def generate_queries(self, query_func, duration_seconds=30):
        start_time = time.time()
        while time.time() - start_time < duration_seconds:
            ciudad = random.choice(CIUDADES_POPULARES)
            query_func()

            if self.model == "uniform":
                time.sleep(1 / self.rate)
            elif self.model == "poisson":
                tiempo_espera = np.random.exponential(1 / self.rate)
                time.sleep(tiempo_espera)
            else:
                raise ValueError(f"Modelo de tráfico desconocido: {self.model}")
