Модель трансформер final_model_train_additional.ipynb 
Inference - Final_CCT_inference.ipynb
Интерпретация модели - final_model_analysis.ipynb
Основная утилита создания датафрейма - dataframe_creation_utility.ipynb

Датафреймы находятся в папке dataframes

**files_pollution.csv** - основная созданная база, соединяет таблицу с загрязнениями и папки с файлами снимков.

**timestamp.csv (timestamp_2021.csv)** - таблица с всеми времеными метами снимков, где были загрязнения в текущем году. Отдельно 2021 год, так как создавался ранее

**clean_pollution.csv** - очищенная таблица зарязнений

**clean_pollution_old.csv** - первая версия, где много не нужных данных, например, даты до 2017 года

**bbox_2021.csv** - таблица bbox снимков, с их именами и координатами

**no_bbox_2021.csv, no_timestamp_2021.csv** - таблицы со списком файлов, где  не нашлось нужных данных

Для запуска веб-сервиса запустите main.py
