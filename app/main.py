import scraper
from storage import Storage
from generator import TrafficGenerator
from cache import CacheLRU, CacheFIFO
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

storage = Storage()

policies = [CacheLRU, CacheFIFO]
rates = [2, 5]


def make_query(cache):
    def query():
        city = random.choice(
            ["Santiago", "Providencia", "Las Condes", "Maipú", "Ñuñoa"]
        )
        logger.info(f"Buscando eventos en {city}...")
        cached_result = cache.get(city)
        if cached_result:
            logger.info(f"Cache HIT para {city}")
        else:
            logger.info(f"Cache MISS para {city}, buscando en la base de datos...")
            result = storage.find_events({"ciudad": city})
            cache.put(city, result)

    return query


if __name__ == "__main__":
    logger.info("Iniciando el scraper...")
    scraper.main_loop()
    time.sleep(5)

    logger.info("Iniciando el generador de tráfico...")
    for policy in policies:
        for rate in rates:
            logger.info(
                f"Probando política de caché: {policy.__name__} con tasa {rate}"
            )

            cache = policy(capacidad=50)
            generator = TrafficGenerator(model="poisson", rate=rate)

            query_func = make_query(cache)
            generator.generate_queries(query_func=query_func, duration_seconds=30)
            time.sleep(5)
