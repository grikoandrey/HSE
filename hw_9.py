import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")

with open("events_hw.json", encoding="utf-8") as f:
    dirty_data = json.load(f)

df = pd.DataFrame(dirty_data["events"])
# Преобразование timestamp в правильный формат
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

print("Исходные данные:")
print(df)
print("Информация о данных:")
print(df.info())

# добавим колонку hour
df["hour"] = df["timestamp"].dt.hour
df["attack_type"] = df["signature"].str.split().str[0]

# создаём холст с двумя графиками
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# График 1 — распределение типов событий
sns.countplot(
    y="signature",
    data=df,
    hue="signature",
    order=df["signature"].value_counts().index,
    palette="rocket",
    dodge=False,
    ax=axes[0]
)
axes[0].set_title("Распределение типов событий ИБ")
axes[0].set_xlabel("Количество")
axes[0].set_ylabel("Тип события")

# График 2 — распределение типов событий
sns.countplot(
    y="attack_type",
    data=df,
    hue="attack_type",
    order=df["attack_type"].value_counts().index,
    palette="Set2",
    dodge=False,
    ax=axes[1]
)
axes[1].set_title("Укрупненное деление событий ИБ")
axes[1].set_xlabel("Количество")
axes[1].set_ylabel("Тип события")

# График 3 — распределение по часам
sns.countplot(
    x="hour",
    data=df,
    hue="hour",
    palette="coolwarm",
    dodge=False,
    ax=axes[2]
)
axes[2].set_title("Распределение событий по часам")
axes[2].set_xlabel("Час")
axes[2].set_ylabel("Количество")

plt.tight_layout()
plt.show()
