# HW06 – Report

> Файл: `homeworks/HW06/report.md`  
> Важно: не меняйте названия разделов (заголовков). Заполняйте текстом и/или вставляйте результаты.

## 1. Dataset

- Какой датасет выбран: `S06-hw-dataset-02.csv`
- Размер: (18000, 39)
- Целевая переменная: `target` ('0' - 74%, '1' - 26%)
- Признаки: числовые

## 2. Protocol

- Разбиение: train/test 80/20, random_state=42
- Подбор: CV на train - 5 фолдов, оптимизировала roc-auc 
- Метрики: accuracy, F1, ROC-AUC, так как исследовалась бинарная классификация

## 3. Models

- DummyClassifier (baseline)
- LogisticRegression (параметр с)
- DecisionTreeClassifier (контроль сложности: `max_depth` + `min_samples_leaf`)
- RandomForestClassifier (max_depth)
- AdaBoost(n_estimators)

## 4. Results

| accuracy |       f1 |   roc_auc |               model |
|----------|----------|-----------|---------------------|
|   0.7375 |   0.0000 |   0.5000  |Dummy(most_frequent) |
|   0.8119 |   0.5607 |   0.7977  |      Log_regression |
|   0.8383 |   0.6576 |   0.8371  |       Decision_tree |
|   0.8656 |   0.6803 |   0.9152  |       Random_forest | 
|   0.8839 |   0.7391 |   0.9237  |            AdaBoost |

- Лучше всего себя показали ансамблевые модели (AdaBoost как самая лучшая), так как они лучше понимают нелинейные зависимости


## 5. Analysis


- Модели `DesicionTree` и `RandomForest` достаточно устойчивы к изменению random state
- confusion matrix для лучшей модели (заметен перекос в классах):
```
[[2590, 65],
[353, 592]]
```
- Из permutation importance видно, что наибольшую важность имеет признак f16.

## 6. Conclusion

В ходе данной практики выяснили, что ансамблевые решения может улучшить точность прогнозирования. Они имеют преимущество перед базовыми моделями, так как лучше понимают нелинейные зависимости. 
 
