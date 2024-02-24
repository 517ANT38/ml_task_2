import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Загрузка данных
clients = pd.read_csv('clients.csv')
train = pd.read_csv('train.csv')
report_dates = pd.read_csv('report_dates.csv')
transactions = pd.read_csv('transactions.csv')

# Объединение данных
data = pd.merge(clients, train, on='user_id')

# Преобразование категориальных признаков в числовые
data['employee_count_nm'] = data['employee_count_nm'].str.extract('(\d+)').astype(float)
data['bankemplstatus'] = data['bankemplstatus'].astype(int)

# Обработка пропусков
data['employee_count_nm'].fillna(data['employee_count_nm'].median(), inplace=True)

# Выбор целевой переменной и признаков
X = data.drop(['user_id', 'target'], axis=1)
y = data['target']

# Разделение данных на обучающий и тестовый набор
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели случайного леса
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Предсказание на тестовом наборе и оценка качества
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
