import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


### Section 1: CoinMarketCap API
def getCoinMarketCapData(limit):
    # CoinMarketCap API key
    cmc_key = "43ae310f-8de6-483f-8130-fd0486d8c3ed"

    # CoinMarketCap API endpoint and parameters
    cmc_endpoint = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    cmc_params = {
        "start": "1",
        "limit": limit,
        "convert": "USD",
        "sort": "market_cap",
        "cryptocurrency_type": "coins",
    }

    # CoinMarketCap API headers
    cmc_headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": cmc_key}

    # Get CoinMarketCap data
    cmc_data = requests.get(
        cmc_endpoint, params=cmc_params, headers=cmc_headers
    ).json()["data"]

    # Create CoinMarketCap dataframe
    cmc_df = pd.DataFrame(cmc_data, columns=["name", "symbol", "slug", "quote"])
    cmc_df["market_cap"] = [quote["USD"]["market_cap"] for quote in cmc_df["quote"]]
    cmc_df["volume_24h"] = [quote["USD"]["volume_24h"] for quote in cmc_df["quote"]]
    cmc_df.drop(columns=["slug", "quote"], inplace=True)
    cmc_df.set_index("symbol", inplace=True)

    # Return CoinMarketCap dataframe
    return cmc_df


### Section 2: CoinGecko API
def getCoinGeckoData(limit):
    # CoinGecko API endpoint and parameters
    cg_endpoint = "https://api.coingecko.com/api/v3"
    cg_params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
    }

    # Get CoinGecko data
    cg_data = requests.get(f"{cg_endpoint}/coins/markets", params=cg_params).json()
    print(cg_data)
    # Create CoinGecko dataframe
    cg_df = pd.DataFrame(
        cg_data, columns=["name", "symbol", "market_cap", "total_volume"]
    )

    # Rename "total_volume" column to "volume_24h"
    cg_df.rename(columns={"total_volume": "volume_24h"}, inplace=True)

    # Make the symbol uppercase
    cg_df["symbol"] = cg_df["symbol"].str.upper()
    cg_df.set_index("symbol", inplace=True)

    # Return CoinGecko dataframe
    return cg_df


### Section 3: Plotting
def plotData(cmc_data, cg_data):
    # Create a unified dataframe
    unified_data = getUnifiedRanking(cmc_data, cg_data)

    # Create a plotly figure
    fig = go.Figure()

    # Add a bar chart for market cap
    fig.add_trace(
        go.Bar(
            x=unified_data.index,
            y=unified_data["weighted_market_cap"] / 1_000_000_000,
            name="Market Cap",
            marker_color="#1f77b4",
            yaxis="y1",
            hovertemplate="Market Cap: %{y:.2f}B USD<br>",
        )
    )

    # Add a line chart for volume 24h
    fig.add_trace(
        go.Scatter(
            x=unified_data.index,
            y=unified_data["weighted_volume_24h"] / 1_000_000_000,
            name="Volume 24h",
            marker_color="#ff7f0e",
            yaxis="y2",
            mode="lines+markers",
            hovertemplate="Volume 24h: %{y:.2f}B USD<br>",
        )
    )

    # Set the layout
    fig.update_layout(
        title="Top 5 Cryptocurrencies by Market Cap and Volume",
        xaxis_title="Cryptocurrency",
        yaxis=dict(title="Market Cap (USD billions)", tickformat=".2fB", side="left"),
        yaxis2=dict(
            title="Volume 24h (USD billions)",
            tickformat=".2fB",
            side="right",
            overlaying="y",
        ),
        legend=dict(x=0, y=1.2, orientation="h"),
    )

    # Return the plotly figure
    return fig


### Section 4: Unified ranking
def getUnifiedRanking(cmc_data, cg_data):
    # Merge data from both sources
    merged_data = pd.merge(
        cmc_data, cg_data, on="symbol", how="outer", suffixes=("_cmc", "_cg")
    )

    # Drop rows with missing data
    merged_data.dropna(inplace=True)

    # Weight for market cap and volume_24h variables from each source
    cmc_weight_market_cap = 0.5
    cmc_weight_volume_24h = 0.5
    cg_weight_market_cap = 1 - cmc_weight_market_cap
    cg_weight_volume_24h = 1 - cmc_weight_volume_24h

    # Calculate weighted scores for market cap and volume_24h variables for each source
    merged_data["weighted_market_cap"] = (
        merged_data["market_cap_cmc"] * cmc_weight_market_cap
    ) + (merged_data["market_cap_cg"] * cg_weight_market_cap)

    merged_data["weighted_volume_24h"] = (
        merged_data["volume_24h_cmc"] * cmc_weight_volume_24h
    ) + (merged_data["volume_24h_cg"] * cg_weight_volume_24h)

    # Sort the dataframe by the weighted market cap in descending order
    merged_data.sort_values(by="weighted_market_cap", ascending=False, inplace=True)

    # Return the unified dataframe
    return merged_data