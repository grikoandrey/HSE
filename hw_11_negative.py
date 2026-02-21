import pandas as pd
from pandas import json_normalize
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
matplotlib.use('TkAgg')

# считывание данных из файлов
df = pd.read_json('botsv1.json')

# Нормализация
logs = json_normalize(df['result'])

# print(df.head(3))
# print(df.columns)
# print('=' * 30)
# print(logs.head(5).to_string())
# print(logs.columns)

# анализируем состав и количество логов
print('=' * 10, 'Анализ вида и количества логов', '=' * 10)
print(logs['LogName'].value_counts())

# Разделяем логи
win_logs = logs[logs['LogName'] == 'Security'].copy()
dns_logs = logs[logs['LogName'] == 'DNS'].copy()
print('=' * 10, 'Разделение логов по видам', '=' * 10)
print("WinEventLog:", win_logs.shape)
print("DNS logs:", dns_logs.shape)

# определение подозрительных логов
suspicious_event_ids = ['4625', '4672', '4688', '4703', '4720']

win_suspicious = win_logs[win_logs['EventCode'].astype(str).isin(suspicious_event_ids)]

# Топ-10 по частоте
win_top10 = win_suspicious['EventCode'].value_counts().head(10)
print('=' * 10, 'Топ 10 подозрительных логов', '=' * 10)
print(win_top10)

# ищем suspicious в eventtype
dns_suspicious = dns_logs[
    dns_logs['eventtype'].astype(str).str.contains('suspicious', na=False)
]

dns_top10 = dns_suspicious['QueryName'].value_counts().head(10)
print(dns_top10)

# Визуализация результатов------------------------
# Преобразуем Series в DataFrame для seaborn
win_top10_df = win_top10.reset_index()
win_top10_df.columns = ['EventCode', 'Count']

dns_top10_df = dns_top10.reset_index()
dns_top10_df.columns = ['QueryName', 'Count']

sns.set_theme(
    style="whitegrid",
    context="talk",        # крупнее текст
    palette="viridis"
)

fig, axes = plt.subplots(2, 1, figsize=(12, 5))

# ----------- WIN EVENTS -----------
sns.barplot(
    data=win_top10_df,
    x='Count',
    y='EventCode',
    ax=axes[0]
)

axes[0].set_title("Топ подозрительных событий", fontsize=12, weight='bold')
axes[0].set_xlabel("кол-во событий")
axes[0].set_ylabel("код события")

# Подписи значений
for container in axes[0].containers:
    axes[0].bar_label(container, padding=8)

# ----------- DNS EVENTS -----------
sns.barplot(
    data=dns_top10_df,
    x='Count',
    y='QueryName',
    ax=axes[1]
)

axes[1].set_title("Топ подозрительных запросов", fontsize=12, weight='bold')
axes[1].set_xlabel("кол-во запросов")
axes[1].set_ylabel("домен")

for container in axes[1].containers:
    axes[1].bar_label(container, padding=5)

plt.tight_layout()
plt.show()
