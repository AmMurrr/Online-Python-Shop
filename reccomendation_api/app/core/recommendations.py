import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

# Загрузка данных из файлов
items = pd.read_csv('/home/artem/python_MAI_project/project/reccomendation_api/app/core/items.csv')
categories = pd.read_csv('/home/artem/python_MAI_project/project/reccomendation_api/app/core/item_categories.csv')

# Объединяем таблицы по общему полю item_category_id
merged_data = items.merge(categories, on='item_category_id', how='left')

# Посчитаем количество покупок каждого товара в каждой категории
item_counts = merged_data.groupby(['item_category_id', 'item_id']).size().reset_index(name='count')

# Подготовка данных для кластеризации
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
category_names = categories['item_category_name']
vectorized_categories = tfidf_vectorizer.fit_transform(category_names)

# Кластеризация категорий
num_clusters = 10
kmeans_model = KMeans(n_clusters=num_clusters, random_state=42).fit(vectorized_categories)
cluster_labels = kmeans_model.labels_

# Добавляем кластеры в таблицу категорий
categories['cluster_label'] = cluster_labels

# Синхронная версия функции для получения рекомендаций
def get_recommendations(item_id, limit=3):
    # Находим категорию товара по его ID
    category_id = merged_data.query("item_id == @item_id")['item_category_id'].values[0]
    cluster = categories.query("item_category_id == @category_id")['cluster_label'].values[0]

    # Получить товары из того же кластера, исключая сам товар
    same_cluster_items = item_counts[item_counts['item_id'].isin(merged_data[merged_data['item_category_id'] == category_id]['item_id'])]
    same_cluster_items = same_cluster_items[same_cluster_items['item_id'] != item_id]  # Исключить сам товар

    # Выбираем случайные товары из того же кластера (исключая сам товар)
    same_cluster_recommendations = same_cluster_items.sample(min(limit, len(same_cluster_items)))
    same_cluster_recommendations = same_cluster_recommendations['item_id'].to_list()

    # Получаем все уникальные кластеры, кроме текущего
    unique_clusters = categories['cluster_label'].unique()
    similar_clusters = unique_clusters[unique_clusters != cluster]

    # Выбираем 3 случайных кластера из похожих
    random_similar_clusters = np.random.choice(similar_clusters, size=min(3, len(similar_clusters)))

    recommendations = []
    
    for random_cluster in random_similar_clusters:
        # Получаем товары из случайного похожего кластера
        cluster_items = item_counts[item_counts['item_id'].isin(merged_data[merged_data['item_category_id'].isin(categories[categories['cluster_label'] == random_cluster]['item_category_id'])]['item_id'])]
        
        # Исключаем сам товар из рекомендаций
        cluster_items = cluster_items[cluster_items['item_id'] != item_id]
        
        # Добавляем случайные товары из этого кластера в рекомендации
        sampled_items = cluster_items.sample(min(limit, len(cluster_items)))['item_id'].to_list()
        recommendations.extend(sampled_items)

    # Удаляем дубликаты и ограничиваем количество рекомендаций
    recommendations = pd.Series(recommendations).drop_duplicates().head(limit).to_list()
    
    # Получаем названия товаров по их ID
    same_cluster_item_names = merged_data[merged_data['item_id'].isin(same_cluster_recommendations)]['item_name'].to_list()
    similar_item_names = merged_data[merged_data['item_id'].isin(recommendations)]['item_name'].to_list()
    
    return same_cluster_item_names, similar_item_names