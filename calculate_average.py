from services.vehicles import calculate_average_price
import pandas as pd 


if __name__ == "__main__":
    results = calculate_average_price()
    df = pd.DataFrame(results, columns=['vehicle_id', 'avg_price'])
    print(df)

