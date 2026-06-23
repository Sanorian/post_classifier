import os
import joblib
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score
from catboost import CatBoostClassifier

CATEGORIES = [
    'rec.sport.hockey', 'rec.sport.baseball',
    'sci.space', 'sci.med',
    'comp.graphics', 'talk.politics.guns',
]
RANDOM_SEED = 42

print("Загрузка данных...")
train_data = fetch_20newsgroups(
    subset='train',
    categories=CATEGORIES,
    remove=('headers', 'footers', 'quotes'),
    shuffle=True,
    random_state=RANDOM_SEED
)
test_data = fetch_20newsgroups(
    subset='test',
    categories=CATEGORIES,
    shuffle=True,
    random_state=RANDOM_SEED
)

X_train, y_train = train_data.data, train_data.target
X_test, y_test = test_data.data, test_data.target
categories = train_data.target_names

print("Векторизация...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=30000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("Обучение LogisticRegression...")
gs = GridSearchCV(
    LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
    param_grid={'C': [1, 5, 10]},
    cv=3,
    scoring='f1_macro',
    n_jobs=-1
)
gs.fit(X_train_tfidf, y_train)
lr_model = gs.best_estimator_
y_pred_lr = lr_model.predict(X_test_tfidf)
f1_lr = f1_score(y_test, y_pred_lr, average='macro')

print("Обучение CatBoost...")
cb_model = CatBoostClassifier(
    loss_function='MultiClass',
    iterations=500,
    learning_rate=0.1,
    depth=6,
    random_seed=RANDOM_SEED,
    verbose=False
)
cb_model.fit(X_train_tfidf, y_train)
y_pred_cb = cb_model.predict(X_test_tfidf)
f1_cb = f1_score(y_test, y_pred_cb, average='macro')

best_model = lr_model if f1_lr >= f1_cb else cb_model
print(f"Лучшая модель: {'LogisticRegression' if f1_lr>=f1_cb else 'CatBoost'}, F1 = {max(f1_lr, f1_cb):.4f}")

# Сохраняем артефакты
os.makedirs('artifacts', exist_ok=True)
joblib.dump(best_model, 'artifacts/model.joblib')
joblib.dump(vectorizer, 'artifacts/vectorizer.joblib')
joblib.dump(categories, 'artifacts/categories.joblib')
print("Артефакты сохранены в папку artifacts/")