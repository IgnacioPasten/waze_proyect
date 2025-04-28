from collections import OrderedDict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheBase:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.cache = OrderedDict()

    def get(self, clave):
        raise NotImplementedError

    def put(self, clave, valor):
        raise NotImplementedError


class CacheLRU(CacheBase):
    def get(self, clave):
        if clave in self.cache:
            self.cache.move_to_end(clave)
            logger.info(f"Cache LRU: buscando {clave}")
            return self.cache[clave]
        return None

    def put(self, clave, valor):
        if clave in self.cache:
            self.cache.move_to_end(clave)
        self.cache[clave] = valor
        if len(self.cache) > self.capacidad:
            logger.info(f"Cache MISS para {clave}, eliminando el menos usado")
            self.cache.popitem(last=False)


class CacheFIFO(CacheBase):
    def get(self, clave):
        logger.info(f"Cache FIFO: buscando {clave}")
        return self.cache.get(clave, None)

    def put(self, clave, valor):
        if clave not in self.cache and len(self.cache) >= self.capacidad:
            logger.info(f"Cache FIFO: eliminando {next(iter(self.cache))}")
            self.cache.popitem(last=False)
        self.cache[clave] = valor
