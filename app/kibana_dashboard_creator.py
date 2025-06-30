import requests
import json
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KibanaDashboardCreator:
    def __init__(self, kibana_host="localhost", kibana_port=5601):
        self.kibana_url = f"http://{kibana_host}:{kibana_port}"
        self.headers = {
            "Content-Type": "application/json",
            "kbn-xsrf": "true"
        }
        
    def wait_for_kibana(self, max_attempts=30, delay=10):
        logger.info("Esperando a que Kibana esté disponible...")
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.kibana_url}/api/status", timeout=5)
                if response.status_code == 200:
                    logger.info("Kibana está disponible")
                    return True
            except Exception:
                pass
            
            logger.info(f"Intento {attempt + 1}/{max_attempts}...")
            time.sleep(delay)
        
        logger.error("Kibana no está disponible después de esperar")
        return False
    
    def create_simple_dashboard(self):
        try:
            dashboard_id = "waze-system-dashboard"
            
            check_url = f"{self.kibana_url}/api/saved_objects/dashboard/{dashboard_id}"
            check_response = requests.get(check_url, headers=self.headers)
            
            if check_response.status_code == 200:
                logger.info(f"Dashboard '{dashboard_id}' ya existe")
                delete_response = requests.delete(check_url, headers=self.headers)
                if delete_response.status_code == 200:
                    logger.info("Dashboard anterior eliminado, creando uno nuevo...")
                else:
                    logger.info("Usando dashboard existente")
                    return True
            
            dashboard_payload = {
                "attributes": {
                    "title": "Sistema de Análisis de Tráfico Waze",
                    "description": "Dashboard principal del sistema de análisis de datos de tráfico con visualizaciones en tiempo real",
                    "panelsJSON": json.dumps([
                        {
                            "version": "8.13.2",
                            "type": "search",
                            "gridData": {
                                "x": 0,
                                "y": 0,
                                "w": 48,
                                "h": 20,
                                "i": "cache-metrics-panel"
                            },
                            "panelIndex": "cache-metrics-panel",
                            "embeddableConfig": {
                                "title": "Métricas de Cache en Tiempo Real",
                                "columns": ["timestamp", "politica", "tasa", "resultado"],
                                "sort": [["timestamp", "desc"]],
                                "hidePanelTitles": False
                            },
                            "panelRefName": "panel_cache-metrics-panel"
                        },
                        {
                            "version": "8.13.2", 
                            "type": "search",
                            "gridData": {
                                "x": 0,
                                "y": 20,
                                "w": 48,
                                "h": 20,
                                "i": "processing-metrics-panel"
                            },
                            "panelIndex": "processing-metrics-panel",
                            "embeddableConfig": {
                                "title": "Métricas de Procesamiento", 
                                "columns": ["timestamp", "eventos_procesados", "tiempo_total", "fase"],
                                "sort": [["timestamp", "desc"]],
                                "hidePanelTitles": False
                            },
                            "panelRefName": "panel_processing-metrics-panel"
                        }
                    ]),
                    "version": 1,
                    "timeRestore": True,
                    "timeTo": "now",
                    "timeFrom": "now-24h",
                    "refreshInterval": {
                        "pause": False,
                        "value": 10000
                    },
                    "kibanaSavedObjectMeta": {
                        "searchSourceJSON": json.dumps({
                            "query": {
                                "query": "",
                                "language": "kuery"
                            },
                            "filter": []
                        })
                    }
                },
                "references": [
                    {
                        "name": "panel_cache-metrics-panel",
                        "type": "search",
                        "id": "cache-discover-search"
                    },
                    {
                        "name": "panel_processing-metrics-panel", 
                        "type": "search",
                        "id": "processing-discover-search"
                    }
                ]
            }
            
            # Primero crear las búsquedas guardadas (saved searches)
            self._create_saved_search("cache-discover-search", 
                                     "Búsqueda de Métricas de Cache",
                                     "cache-metrics-pattern",
                                     ["timestamp", "politica", "tasa", "resultado"])
            
            self._create_saved_search("processing-discover-search",
                                     "Búsqueda de Métricas de Procesamiento", 
                                     "pipeline-metrics-pattern",
                                     ["timestamp", "eventos_procesados", "tiempo_total", "fase"])
            
            # Crear el dashboard
            url = f"{self.kibana_url}/api/saved_objects/dashboard/{dashboard_id}"
            response = requests.post(url, headers=self.headers, json=dashboard_payload)
            
            if response.status_code in [200, 201]:
                logger.info("Dashboard 'Sistema de Análisis de Tráfico Waze' creado exitosamente")
                logger.info(f"Accede a: {self.kibana_url}/app/dashboards#/view/{dashboard_id}")
                return True
            else:
                logger.error(f"Error creando dashboard: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creando dashboard: {e}")
            return False
    
    def _create_saved_search(self, search_id, title, index_pattern_id, columns):
        """Crear una búsqueda guardada para usar en el dashboard"""
        try:
            # Verificar si ya existe
            check_url = f"{self.kibana_url}/api/saved_objects/search/{search_id}"
            check_response = requests.get(check_url, headers=self.headers)
            
            if check_response.status_code == 200:
                logger.info(f"Búsqueda guardada '{search_id}' ya existe")
                return True
            
            # Crear búsqueda guardada
            search_payload = {
                "attributes": {
                    "title": title,
                    "description": f"Búsqueda para visualizar datos de {title}",
                    "hits": 0,
                    "columns": columns,
                    "sort": [["timestamp", "desc"]],
                    "version": 1,
                    "kibanaSavedObjectMeta": {
                        "searchSourceJSON": json.dumps({
                            "index": index_pattern_id,
                            "query": {
                                "query": "",
                                "language": "kuery"
                            },
                            "filter": [],
                            "highlightAll": True,
                            "version": True
                        })
                    }
                },
                "references": [
                    {
                        "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                        "type": "index-pattern",
                        "id": index_pattern_id
                    }
                ]
            }
            
            url = f"{self.kibana_url}/api/saved_objects/search/{search_id}"
            response = requests.post(url, headers=self.headers, json=search_payload)
            
            if response.status_code in [200, 201]:
                logger.info(f"Búsqueda guardada '{title}' creada exitosamente")
                return True
            else:
                logger.error(f"Error creando búsqueda guardada '{title}': {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error creando búsqueda guardada '{search_id}': {e}")
            return False
    
    def setup_complete_dashboard(self):
        logger.info("iniciando configuracion del dashboard de kibana...")
        
        if not self.wait_for_kibana():
            return False
        
        logger.info("creando dashboard...")
        if self.create_simple_dashboard():
            logger.info("dashboard creado exitosamente")
            logger.info(f"accede a Kibana en: {self.kibana_url}")
            logger.info("ve a 'Stack Management' > 'Data Views' para verificar los data views")
            logger.info("ve a 'Dashboards' para ver el dashboard")
            return True
        else:
            logger.error("error creando dashboard")
            return False

def main():
    setup = KibanaDashboardCreator()
    setup.setup_complete_dashboard()

if __name__ == "__main__":
    main()
