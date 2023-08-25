def unix_time(year, month, day, hour, second):
    import datetime
    import time
    date_time = datetime.datetime(year, month, day, hour, second)
    return time.mktime(date_time.timetuple())


def human_time(unix_time):
    import datetime
    return datetime.datetime.fromtimestamp(unix_time)


def get_coin_data(coin_id):
    '''
    
    '''
    from pycoingecko import CoinGeckoAPI
    cg = CoinGeckoAPI()
    data = cg.get_coin_by_id(coin_id, market_data='true', sparkline='true')
    return data


def create_combined_dataframe(coin_data_list):
    import pandas as pd
    dfs = []
    for coin_data in coin_data_list:
        df = pd.DataFrame.from_dict(coin_data, orient='index', columns=[f'data_{coin_data["id"]}'])
        dfs.append(df)
    df_final = pd.concat(dfs, axis=1)
    return df_final



def get_coin_market_dataframe (data):
    import pandas as pd
    # Convertir los datos en un DataFrame
    df = pd.DataFrame()

    for key, values in data.items():
        timestamps = [x[0] for x in values]
        values = [x[1] for x in values]
        
        df_key = pd.DataFrame({
            'timestamp': timestamps,
            key: values
        })
        
        if df.empty:
            df = df_key
        else:
            df = pd.merge(df, df_key, on='timestamp')

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Aplicar el formato a las columnas específicas
    formatted_df = df[['prices', 'market_caps', 'total_volumes']].applymap(lambda x: '{:.2f}'.format(x))

    # Mantener la columna 'timestamp' sin cambios
    formatted_df.insert(0, 'timestamp', df['timestamp'])

    return formatted_df



def coin_ohlc(crypto_coin):
    from pycoingecko import CoinGeckoAPI
    import pandas as pd

    cg = CoinGeckoAPI()
    
    bitcoin_ohlc = cg.get_coin_ohlc_by_id(
    id=crypto_coin, vs_currency="usd", days="max", precision = 2
    )
    df = pd.DataFrame(bitcoin_ohlc)
    df.columns = ["date", "open", "high", "low", "close"]
    df["date"] = pd.to_datetime(df["date"], unit="ms")

    return df


def coin_market_chart_data(coin, start_time, end_time):
    from pycoingecko import CoinGeckoAPI
    cg = CoinGeckoAPI()

    data = cg.get_coin_market_chart_range_by_id(
        id=coin,
        vs_currency="usd",
        from_timestamp=start_time,
        to_timestamp=end_time
    )

    return data