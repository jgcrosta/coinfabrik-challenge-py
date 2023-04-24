from challenge import getCoinGeckoData, getCoinMarketCapData, plotData

# Amount of cryptos to read
amount_to_read = 300

# Get data from CoinMarketCap and CoinGecko
cmc_data = getCoinMarketCapData(amount_to_read)
cg_data = getCoinGeckoData(amount_to_read)

# Data to csv
cmc_data.to_csv("cmc_data.csv")
cg_data.to_csv("cg_data.csv")

# Plot data
plotData(cmc_data, cg_data)