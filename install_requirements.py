import subprocess
import sys
import os

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} instalado correctamente")
        return True
    except subprocess.CalledProcessError:
        print(f"error instalando {package}")
        return False

def main():
    print("instalando dependencias del sistema Waze...")
    print("=" * 50)
    
    # Lista de paquetes
    packages = [
        "pymongo",
        "elasticsearch>=7.0.0,<8.0.0",
        "requests",
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "schedule",
        "psutil",
        "flask",
        "plotly",
        "beautifulsoup4",
        "selenium",
        "webdriver-manager"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"instalando {package}...")
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    
    if failed_packages:
        print(f"algunos paquetes no se pudieron instalar:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\n puedes intentar instalarlos manualmente con:")
        print(f"   pip install {' '.join(failed_packages)}")
    else:
        print("todas las dependencias instaladas correctamente!")
        print("el sistema esta listo para ejecutarse")
    
    print("\n para ejecutar el sistema completo:")
    print("   cd app")
    print("   python main.py")
    print("\n para acceder a las visualizaciones:")
    print("   Kibana: http://localhost:5601")
    print("   Elasticsearch: http://localhost:9200")

if __name__ == "__main__":
    main()
