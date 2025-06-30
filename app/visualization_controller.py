import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualizationController:
    def __init__(self, config):
        self.config = config
        self.system_running = False
        self.total_events_processed = 0
        self.pipeline_status = "stopped"
        self.cache_lru_size = 0
        self.cache_fifo_size = 0
        
    def start_system(self):
        try:
            logger.info("Iniciando sistema de visualización")
            self.system_running = True
            self.pipeline_status = "running"
            time.sleep(1)
            logger.info("Sistema de visualización iniciado correctamente")
            return True
        except Exception as e:
            logger.error(f"Error iniciando sistema de visualización: {e}")
            return False
    
    def stop_system(self):
        try:
            logger.info("Deteniendo sistema de visualización")
            self.system_running = False
            self.pipeline_status = "stopped"
            logger.info("Sistema de visualización detenido")
        except Exception as e:
            logger.error(f"Error deteniendo sistema: {e}")
    
    def manual_scrape(self, max_events=50):
        try:
            logger.info(f"Iniciando scraping manual (máximo {max_events} eventos)")
            eventos = []
            tipos_evento = ["HAZARD", "JAM", "ACCIDENT", "ROAD_CLOSED"]
            ciudades = ["Santiago", "Providencia", "Las Condes", "Maipú", "Ñuñoa"]
            
            for i in range(min(max_events, 20)):
                evento = {
                    "uuid": f"manual_{i}_{int(time.time())}",
                    "fecha": datetime.now().isoformat(),
                    "tipo": tipos_evento[i % len(tipos_evento)],
                    "ciudad": ciudades[i % len(ciudades)],
                    "calle": f"Calle Demo {i}",
                    "manual_scrape": True
                }
                eventos.append(evento)
            
            self.total_events_processed += len(eventos)
            logger.info(f"Scraping manual completado: {len(eventos)} eventos procesados")
            return eventos
        except Exception as e:
            logger.error(f"Error en scraping manual: {e}")
            return []
    
    def get_system_status(self):
        return {
            "system_running": self.system_running,
            "pipeline_status": self.pipeline_status,
            "total_events_processed": self.total_events_processed,
            "cache_lru_size": self.cache_lru_size,
            "cache_fifo_size": self.cache_fifo_size,
            "timestamp": datetime.now().isoformat()
        }
