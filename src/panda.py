import re
from pathlib import Path
import pandas as pd
import sqlite3
class EmployeeLoader:
    def __init__(self, file):
        self.file = file

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.file)
        df['Date of birth'] = pd.to_datetime(
            df['Date of birth'],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        )

        today = pd.Timestamp.now()
        future_dates = (df['Date of birth'] > today) & df['Date of birth'].notna()
        df.loc[future_dates, 'Date of birth'] = df.loc[future_dates, 'Date of birth'].apply(
            lambda dt: dt.replace(year=dt.year - 100)
        )
        df['Age'] = (today - df['Date of birth']).dt.days // 365.25

        phone_nums =df['Phone'].astype(str)
        df['Extension'] = phone_nums.str.extract(r'[xX](\d+)',expand=False) #extract text using pattern: r(raw str), xX (lower/uppercase of x, \d capture all digits after x or X
        clean_nums = phone_nums.str.split(r'[xX]').str[0] #splits anything after x
        clean_nums = clean_nums.str.replace(r'\D','',regex=True) #replace any non digit (r'\D') with '' (empty text)
        df['Phone'] = clean_nums.apply(lambda x: f"{x[-10:-7]}-{x[-7:-4]}-{x[-4:]}" if len(x) >=10 else None)#lambda x loop through every str x in clean_nums and apply the following f"{x[-10:-7]}-{x[-7:-4]}-{x[-4:]}" if length >=10

        return df

    def save_data(self, df: pd.DataFrame, output_file: str):
        df.to_excel(output_file, index=False)
        print(f"File saved successfully as '{output_file}'!")

class EmployeeAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def count_gender(self) -> dict:
        return self.df['Sex'].value_counts().to_dict()

    def top_jobs(self, limit=5) -> dict:
        return self.df['Job Title'].value_counts().head(limit).to_dict()
    def median_age(self) -> float:
        return self.df['Age'].median()
    def avg_age(self) -> float:
        return self.df['Age'].mean()
    def rand_phone_nums(self) -> dict:
        print(df[['Phone', 'Extension']].sample(5))

if __name__ == '__main__':
    DATA_DIR = Path(__file__).parent.parent / "data"
    loader = EmployeeLoader(DATA_DIR / "Employee 1000x.csv")
    df = loader.load_data()
    analyzer = EmployeeAnalysis(df)
    print("Gender Distribution:", analyzer.count_gender())
    print("Top 5 Job Titles:", analyzer.top_jobs(5))
    print("Median Age:", analyzer.median_age())
    print("Average Age:", analyzer.avg_age())
    #analyzer.rand_phone_nums()
    loader.save_data(df, "Employee_1000x_Cleaned.xlsx")

    conn = sqlite3.connect('employee.db')
    df.to_sql('employee', conn, if_exists='replace', index=False)

    result  = pd.read_sql_query('select * from employee', conn)
    print(result)

    conn.close()