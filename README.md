# CoinGecko/CoinMarketCap API - Python

## challenge.py

- getCoinMarketCapData(limit): obtiene los datos más recientes de las criptomonedas de CoinMarketCap a través de su API y devuelve un DataFrame de Pandas con los campos 'name', 'symbol', 'market_cap' y 'volume_24h' para cada criptomoneda.
- getCoinGeckoData(limit): obtiene los datos más recientes de las criptomonedas de CoinGecko a través de su API y devuelve un DataFrame de Pandas con los campos 'name', 'symbol', 'market_cap' y 'volume_24h' para cada criptomoneda.
- getUnifiedRanking(cmc_data, cg_data): fusiona los datos de CoinMarketCap y CoinGecko y devuelve un DataFrame de Pandas con las mismas columnas que las funciones anteriores.
- plotData(cmc_data, cg_data): toma los datos fusionados de CoinMarketCap y CoinGecko, los procesa para generar una gráfica y devuelve una figura de Plotly.

## converter.py

Este código carga un archivo llamado "cg_data.csv" utilizando la biblioteca Pandas de Python, convierte los datos a un diccionario de Python y luego a una cadena de JSON. A continuación, se convierte la cadena de JSON en un objeto de TypeScript, y se guarda en un archivo llamado "cg_data.ts". El objeto TypeScript generado tiene una interfaz denominada "LatestResponse" que define la estructura de los datos.

## main.py

El código proporcionado carga datos de CoinMarketCap y CoinGecko, y luego los guarda como archivos CSV. 
