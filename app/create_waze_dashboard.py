import requests
import json
import time

KIBANA_URL = "http://localhost:5601"
ELASTICSEARCH_URL = "http://localhost:9200"

def refresh_index_pattern():
    print("refrescando index pattern...")
    
    try:
        response = requests.get(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/cache-metrics-real",
            headers={"kbn-xsrf": "true"}
        )
        
        if response.status_code == 200:
            pattern_data = response.json()
            
            pattern_data['attributes']['fields'] = json.dumps([
                {
                    "name": "timestamp",
                    "type": "date",
                    "searchable": True,
                    "aggregatable": True
                },
                {
                    "name": "politica",
                    "type": "string",
                    "searchable": True,
                    "aggregatable": True
                },
                {
                    "name": "resultado",
                    "type": "string",
                    "searchable": True,
                    "aggregatable": True
                },
                {
                    "name": "tasa",
                    "type": "number",
                    "searchable": True,
                    "aggregatable": True
                },
                {
                    "name": "ciudad",
                    "type": "string",
                    "searchable": True,
                    "aggregatable": True
                }
            ])
            
            update_response = requests.put(
                f"{KIBANA_URL}/api/saved_objects/index-pattern/cache-metrics-real",
                headers={
                    "Content-Type": "application/json",
                    "kbn-xsrf": "true"
                },
                json={"attributes": pattern_data['attributes']}
            )
            
            if update_response.status_code in [200, 201]:
                print("Index pattern actualizado")
                return True
            else:
                print(f"error actualizando index pattern: {update_response.status_code}")
        
        refresh_response = requests.post(
            f"{KIBANA_URL}/api/index_patterns/_fields_for_wildcard",
            headers={
                "Content-Type": "application/json",
                "kbn-xsrf": "true"
            },
            json={
                "pattern": "cache_metrics*",
                "meta_fields": ["_source", "_id", "_type", "_index", "_score"]
            }
        )
        
        if refresh_response.status_code == 200:
            print("campos refrescados")
            return True
        else:
            print(f"error refrescando campos: {refresh_response.status_code}")
            
    except Exception as e:
        print(f"error: {e}")
    
    return False

def create_working_pie_chart():
    print("creando piechart...")
    
    try:
        delete_response = requests.delete(
            f"{KIBANA_URL}/api/saved_objects/visualization/cache-pie-working-fixed",
            headers={"kbn-xsrf": "true"}
        )
        print("visualización anterior eliminada (si existía antes)")
    except:
        pass
    
    vis_state = {
        "title": "Cache Hits vs Misses - WORKING",
        "type": "pie",
        "params": {
            "addTooltip": True,
            "addLegend": True,
            "legendPosition": "right",
            "isDonut": False
        },
        "aggs": [
            {
                "id": "1",
                "enabled": True,
                "type": "count",
                "schema": "metric",
                "params": {}
            },
            {
                "id": "2", 
                "enabled": True,
                "type": "terms",
                "schema": "segment",
                "params": {
                    "field": "resultado.keyword",
                    "size": 10,
                    "order": "desc",
                    "orderBy": "1"
                }
            }
        ]
    }
    
    search_source = {
        "index": "cache-metrics-real",
        "query": {
            "bool": {
                "must": [
                    {"match_all": {}}
                ]
            }
        },
        "filter": []
    }
    
    visualization = {
        "attributes": {
            "title": "Cache Hits vs Misses - WORKING",
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "Pie chart para cache hits/misses",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps(search_source)
            }
        },
        "references": [
            {
                "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                "type": "index-pattern",
                "id": "cache-metrics-real"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/visualization/cache-pie-working-fixed",
            headers={
                "Content-Type": "application/json",
                "kbn-xsrf": "true"
            },
            json=visualization
        )
        
        if response.status_code in [200, 201]:
            print("Pie chart working creado/actualizado")
            return True
        else:
            print(f"Error creando pie chart: {response.status_code}")
            print(response.text[:200])
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def create_working_bar_chart():
    print("creando bar chart...")
    
    try:
        delete_response = requests.delete(
            f"{KIBANA_URL}/api/saved_objects/visualization/cache-bar-working-fixed",
            headers={"kbn-xsrf": "true"}
        )
        print("visualización anterior eliminada (si existía antes)")
    except:
        pass
    
    vis_state = {
        "title": "LRU vs FIFO - WORKING",
        "type": "histogram",
        "params": {
            "grid": {"categoryLines": False, "style": {"color": "#eee"}},
            "categoryAxes": [{
                "id": "CategoryAxis-1",
                "type": "category",
                "position": "bottom",
                "show": True,
                "style": {},
                "scale": {"type": "linear"},
                "labels": {"show": True, "truncate": 100},
                "title": {}
            }],
            "valueAxes": [{
                "id": "ValueAxis-1",
                "name": "LeftAxis-1", 
                "type": "value",
                "position": "left",
                "show": True,
                "style": {},
                "scale": {"type": "linear", "mode": "normal"},
                "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                "title": {"text": "Count"}
            }],
            "seriesParams": [{
                "show": True,
                "type": "histogram",
                "mode": "stacked",
                "data": {"label": "Count", "id": "1"},
                "valueAxis": "ValueAxis-1"
            }],
            "addTooltip": True,
            "addLegend": True,
            "legendPosition": "right",
            "times": [],
            "addTimeMarker": False
        },
        "aggs": [
            {
                "id": "1",
                "enabled": True,
                "type": "count",
                "schema": "metric",
                "params": {}
            },
            {
                "id": "2",
                "enabled": True,
                "type": "terms",
                "schema": "segment",
                "params": {
                    "field": "politica.keyword",
                    "size": 10,
                    "order": "desc",
                    "orderBy": "1"
                }
            }
        ]
    }
    
    search_source = {
        "index": "cache-metrics-real",
        "query": {
            "bool": {
                "must": [
                    {"match_all": {}}
                ]
            }
        },
        "filter": []
    }
    
    visualization = {
        "attributes": {
            "title": "LRU vs FIFO - WORKING",
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "Bar chart para políticas de cache",
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps(search_source)
            }
        },
        "references": [
            {
                "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
                "type": "index-pattern",
                "id": "cache-metrics-real"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/visualization/cache-bar-working-fixed",
            headers={
                "Content-Type": "application/json",
                "kbn-xsrf": "true"
            },
            json=visualization
        )
        
        if response.status_code in [200, 201]:
            print("Bar chart working creado/actualizado")
            return True
        else:
            print(f"Error creando bar chart: {response.status_code}")
            print(response.text[:200])
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def create_test_dashboard():
    print("creando dashboard...")
    
    try:
        delete_response = requests.delete(
            f"{KIBANA_URL}/api/saved_objects/dashboard/dashboard-graphics-waze",
            headers={"kbn-xsrf": "true"}
        )
        print("dashboard anterior eliminado (si existía antes)")
    except:
        pass
    
    dashboard = {
        "attributes": {
            "title": "dashboard graphics waze",
            "description": "graficos obtenidos",
            "panelsJSON": json.dumps([
                {
                    "version": "8.13.2",
                    "type": "visualization",
                    "gridData": {"x": 0, "y": 0, "w": 24, "h": 20, "i": "panel-1"},
                    "panelIndex": "panel-1",
                    "embeddableConfig": {"title": "Cache Hits vs Misses"},
                    "panelRefName": "panel_panel-1"
                },
                {
                    "version": "8.13.2",
                    "type": "visualization",
                    "gridData": {"x": 24, "y": 0, "w": 24, "h": 20, "i": "panel-2"},
                    "panelIndex": "panel-2", 
                    "embeddableConfig": {"title": "LRU vs FIFO"},
                    "panelRefName": "panel_panel-2"
                }
            ]),
            "timeRestore": False,
            "version": 1,
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({
                    "query": {"query": "", "language": "kuery"},
                    "filter": []
                })
            }
        },
        "references": [
            {
                "name": "panel_panel-1",
                "type": "visualization",
                "id": "cache-pie-working-fixed"
            },
            {
                "name": "panel_panel-2",
                "type": "visualization", 
                "id": "cache-bar-working-fixed"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/dashboard/dashboard-graphics-waze",
            headers={
                "Content-Type": "application/json",
                "kbn-xsrf": "true"
            },
            json=dashboard
        )
        
        if response.status_code in [200, 201]:
            print("dashboard creado/actualizado")
            print(f"URL: {KIBANA_URL}/app/dashboards#/view/dashboard-graphics-waze")
            return True
        else:
            print(f"Error creando dashboard: {response.status_code}")
            print(response.text[:200])
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_data_access():
    print("probando acceso a datos...")
    
    try:
        query = {
            "size": 0,
            "aggs": {
                "by_resultado": {
                    "terms": {"field": "resultado.keyword"}
                }
            }
        }
        
        response = requests.get(
            f"{ELASTICSEARCH_URL}/cache_metrics/_search",
            headers={"Content-Type": "application/json"},
            json=query
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total documentos: {data['hits']['total']['value']}")
            
            if 'aggregations' in data:
                buckets = data['aggregations']['by_resultado']['buckets']
                print("Distribucion por resultado:")
                for bucket in buckets:
                    print(f"   {bucket['key']}: {bucket['doc_count']} documentos")
                return True
            else:
                print("no se encontraron aggregations")
        else:
            print(f"error en query: {response.status_code}")
            
    except Exception as e:
        print(f"error: {e}")
    
    return False

def create_index_pattern():
    print("creando index pattern cache-metrics-real...")
    
    try:
        check_response = requests.get(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/cache-metrics-real",
            headers={"kbn-xsrf": "true"}
        )
        
        if check_response.status_code == 200:
            print("Index pattern ya existe")
            return True
        
        index_pattern = {
            "attributes": {
                "title": "cache_metrics*",
                "timeFieldName": "timestamp",
                "fields": json.dumps([
                    {
                        "name": "timestamp",
                        "type": "date",
                        "searchable": True,
                        "aggregatable": True
                    },
                    {
                        "name": "politica",
                        "type": "string",
                        "searchable": True,
                        "aggregatable": True
                    },
                    {
                        "name": "resultado", 
                        "type": "string",
                        "searchable": True,
                        "aggregatable": True
                    },
                    {
                        "name": "tasa",
                        "type": "number",
                        "searchable": True,
                        "aggregatable": True
                    }
                ])
            }
        }
        
        response = requests.post(
            f"{KIBANA_URL}/api/saved_objects/index-pattern/cache-metrics-real",
            headers={
                "Content-Type": "application/json",
                "kbn-xsrf": "true"
            },
            json=index_pattern
        )
        
        if response.status_code in [200, 201]:
            print("Index pattern creado exitosamente")
            return True
        else:
            print(f"error creando index pattern: {response.status_code}")
            print(response.text[:200])
            return False
            
    except Exception as e:
        print(f"error: {e}")
        return False

def main():
    print("SOLUCIONANDO PROBLEMA DE VISUALIZACIONES")
    print("=" * 60)
    
    if not test_data_access():
        print("ERROR: no se puede acceder a los datos")
        return
    
    if not create_index_pattern():
        print("ERROR: no se pudo crear el index pattern")
        return
    
    refresh_index_pattern()
    time.sleep(2)
    
    pie_ok = create_working_pie_chart()
    time.sleep(1)
    
    bar_ok = create_working_bar_chart()
    time.sleep(1)
    
    if pie_ok and bar_ok:
        dashboard_ok = create_test_dashboard()
        
        if dashboard_ok:
            print("\n" + "=" * 60)
            print("DASHBOARD CREADO!")
            print("Abrir en: http://localhost:5601/app/dashboards#/view/dashboard-graphics-waze")
            print("=" * 60)
        else:
            print("error creando dashboard!")
    else:
        print("error creando visualizaciones!")

if __name__ == "__main__":
    main()
