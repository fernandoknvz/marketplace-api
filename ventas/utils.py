# ventas/utils.py
# utils.py
import requests

def obtener_dolar_a_clp():
    API_KEY = "1ced5ef7a167b4eeb5c8e26d"  # Usa tu clave directamente
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["conversion_rates"]["CLP"]

    except requests.exceptions.RequestException as e:
        # Puedes loguear el error si quieres:
        print("Error al obtener la tasa:", e)
        return None
