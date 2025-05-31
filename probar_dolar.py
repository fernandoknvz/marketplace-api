import requests

def obtener_dolar_a_clp():
    API_KEY = "TU_API_KEY"
    url = f"https://v6.exchangerate-api.com/v6/{'1ced5ef7a167b4eeb5c8e26d'}/latest/USD"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["conversion_rates"]["CLP"]
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

print("Dólar a CLP:", obtener_dolar_a_clp())
