import pandas as pd
from scipy.stats import zscore

# Data

df_all = pd.read_csv("all_data.csv", sep=";")
print(len(df_all))

df = df_all[['name', 'isin', 'country', 'gics_sector_name', 'industry_group', # colonnes de base
            'E_SCORE', 'S_SCORE', 'G_SCORE', # scores pilliers esg
            'ODD_13', 'ODD_14', 'ODD_15', # les 3 odd qui nous intéressent
            'ROIC', 'PB ratio', 'FCF yield', # quelques métriques financières pour construire les facteurs
            'VaR 95% 5Y', 'CVaR 95% 5Y', 'Max drawdown 5Y', 'Sharpe 5Y', 'Volatility 5Y', 'Annualized return 5Y' # metriques perf/risques
            ]] 
# Récupérer un historique de prix pour avoir le momentum

# Exclusions sectorielles
df = df[~df['industry_group'].isin(['Oil&Gas', 'Oil&Gas Services', 'Gas'])]
print(len(df))

# Exclusions valeurs ESG et controverses
df = df[df['E_SCORE'].astype(float) >= 3]
df = df[df['S_SCORE'].astype(float) >= 3]
df = df[df['G_SCORE'].astype(float) >= 3]

print(len(df))

df = df.dropna().reset_index(drop=True)
print(len(df))


cols = [x for x in df.columns if x not in ['name', 'isin', 'country', 'gics_sector_name', 'industry_group',
'VaR 95% 5Y', 'CVaR 95% 5Y', 'Max drawdown 5Y', 'Sharpe 5Y', 'Volatility 5Y', 'Annualized return 5Y']]

for factor in cols:

    zscore_col = f'Zscore {factor}'
    quartile_col = f'Fractile {factor}'

    df[zscore_col] = zscore(df[factor].astype(float))
    print(df[zscore_col].value_counts())
    df[quartile_col] = pd.qcut(df[zscore_col], q=4, labels=[x+1 for x in range(4)], duplicates='drop')

df.to_excel("Miaou.xlsx", index=False)