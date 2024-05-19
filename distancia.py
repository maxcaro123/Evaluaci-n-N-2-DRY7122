import requests

# Configura tu API key de GraphHopper
GH_API_KEY = "a2ddb1b2-dd35-42fd-94b0-3c6e62c33b2b"

# Función para obtener las coordenadas geográficas de una ciudad
def obtener_coordenadas(ciudad):
    url = f"https://nominatim.openstreetmap.org/search?format=json&city={ciudad}&country=Chile"
    response = requests.get(url)
    try:
        data = response.json()
    except ValueError:
        raise ValueError(f"Respuesta inválida de la API Nominatim para la ciudad '{ciudad}'. La respuesta fue: {response.text}")

    if response.status_code == 200 and data:
        # Seleccionar la primera coincidencia y obtener las coordenadas
        latitud = data[0]['lat']
        longitud = data[0]['lon']
        return latitud, longitud
    else:
        raise ValueError("No se pudieron obtener las coordenadas de la ciudad.")

# Función para obtener la distancia, duración y narrativa del viaje entre dos ciudades
def obtener_datos_viaje(origen, destino):
    origen_lat, origen_lon = obtener_coordenadas(origen)
    destino_lat, destino_lon = obtener_coordenadas(destino)

    url = f"https://graphhopper.com/api/1/route?point={origen_lat},{origen_lon}&point={destino_lat},{destino_lon}&vehicle=car&locale=es&key={GH_API_KEY}"
    response = requests.get(url)
    try:
        data = response.json()
    except ValueError:
        raise ValueError(f"Respuesta inválida de la API GraphHopper. La respuesta fue: {response.text}")

    if response.status_code == 200 and 'paths' in data:
        path = data['paths'][0]
        distancia_km = path['distance'] / 1000.0  # Convertir de metros a kilómetros
        duracion_segundos = path['time'] / 1000.0  # Convertir de milisegundos a segundos
        narrativa = path['instructions']
        return distancia_km, duracion_segundos, narrativa
    else:
        error_message = data.get('message', 'No se pudo obtener la ruta.')
        raise ValueError(f"Error de la API: {error_message}")

# Función para calcular el consumo de combustible
def calcular_combustible(distancia_km, consumo_por_km=0.08):
    # Suponemos un consumo promedio de 8 litros cada 100 km (0.08 litros por km)
    return distancia_km * consumo_por_km

# Función para imprimir la narrativa del viaje
def imprimir_narrativa(narrativa):
    print("\nNarrativa del viaje:")
    for step in narrativa:
        print(step['text'])

# Función principal
def main():
    print("Bienvenido al calculador de viajes")
    while True:
        origen = input("Ingrese la Ciudad de Origen (o 'q' para salir): ").strip()
        if origen.lower() == 'q':
            print("Saliendo del programa.")
            break
        destino = input("Ingrese la Ciudad de Destino (o 'q' para salir): ").strip()
        if destino.lower() == 'q':
            print("Saliendo del programa.")
            break

        try:
            distancia_km, duracion_segundos, narrativa = obtener_datos_viaje(origen, destino)
            duracion_horas = int(duracion_segundos // 3600)
            duracion_minutos = int((duracion_segundos % 3600) // 60)
            duracion_restante_segundos = int(duracion_segundos % 60)
            combustible_litros = calcular_combustible(distancia_km)

            print(f"\nDistancia entre {origen} y {destino}: {distancia_km:.2f} km")
            print(f"Duración del viaje: {duracion_horas} horas, {duracion_minutos} minutos y {duracion_restante_segundos} segundos")
            print(f"Combustible requerido: {combustible_litros:.2f} litros")
            
            imprimir_narrativa(narrativa)

        except ValueError as e:
            print(e)
        except Exception as e:
            print("Error al obtener los datos del viaje:", e)

if __name__ == "__main__":
    main()

