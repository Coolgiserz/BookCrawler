import pandas as pd

def read_data(csv_path):
    df = pd.read_csv(csv_path,  sep=';;;', header=None, engine='python')
    df.columns = ['id', 'name', 'price', 'link']
    return df


if __name__ == '__main__':
    df = pd.read_csv("../result/data_汉英口译_1.csv", sep=';;;', header=None, engine='python')
    # df = pd.read_csv("../result/data_汉英口译_1.csv")

    print(df)