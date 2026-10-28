# LP-III : Machine Learning (ML)

Each folder has: the **notebook (.ipynb, already executed with outputs)**, the **dataset (.csv)** and an **.html copy**. The HTML opens in any browser and shows all outputs and graphs, which is handy if Jupyter isn't working.

| # | Problem statement | Folder | Key result (already in notebook) |
|---|---|---|---|
| 1 | Uber fare prediction: pre-process, outliers, correlation, Linear Regression vs Random Forest, R2/RMSE | `A1_Uber_Fare_Prediction` | LR R2 0.67, RMSE 2.14 · RF R2 0.74, RMSE 1.91 |
| 2 | Email spam classification using KNN and SVM | `A2_Email_Spam_KNN_SVM` | KNN 83% · SVM 97% |
| 3 | Bank customer churn with a Neural Network (normalize, build, improve, accuracy + confusion matrix) | `A3_Bank_Churn_Neural_Network` | base 82% → improved 86% |
| 4 | Gradient Descent: local minima of y=(x+3)² from x=2 | `A4_Gradient_Descent` | x → −3, y → 0 |
| 5 | KNN on diabetes.csv: confusion matrix, accuracy, error rate, precision, recall | `A5_KNN_Diabetes` | acc 77%, error 23% |
| 6 | K-Means / hierarchical clustering on sales_data_sample.csv; elbow method | `A6_KMeans_Sales` | elbow at K = 3 |
| 7 | Mini project: Titanic survival prediction (Logistic Regression) | `A7_MiniProject_Titanic_Logistic_Regression` | 81% |

## How to run
```bash
pip install numpy pandas matplotlib seaborn scikit-learn jupyter    # only if missing
pip install tensorflow                                              # only for A3 (optional)
jupyter notebook          # then open the folder → notebook → Kernel → Restart & Run All
```
- **Always open the notebook from its own folder.** The CSVs are read with relative paths (`pd.read_csv('uber.csv')`).
- No TensorFlow on the lab PC? A3 detects that and automatically uses scikit-learn's `MLPClassifier` neural network (same ~86% accuracy).
- A1 Random Forest takes about 30–60 s on a lab PC.
- Google Colab also works: upload the notebook + CSV → Run all.

## Viva quick answers
- **Supervised** (labels: regression, classification) vs **Unsupervised** (no labels: clustering).
- **Linear Regression:** y = mx + c, minimizes squared error. **Random Forest:** ensemble of decision trees (bagging), averages predictions, handles non-linearity.
- **R²** = 1 − SS_res/SS_tot (closer to 1 is better). **RMSE** = √mean((y−ŷ)²) (lower is better, same unit as y). **MAE** = mean|y−ŷ|.
- **Outliers:** IQR rule: outside [Q1 − 1.5·IQR, Q3 + 1.5·IQR]. Detect with boxplots.
- **Correlation:** Pearson r ∈ [−1, 1]; heatmap with `df.corr()`.
- **KNN:** lazy learner. Classify by majority vote of the K nearest points (Euclidean distance). Needs feature scaling. Choose odd K. Small K overfits, large K underfits.
- **SVM:** finds the maximum-margin hyperplane. Support vectors are the closest points. Kernels: linear, RBF, polynomial. C = regularization.
- **Confusion matrix:** TP, TN, FP, FN. Accuracy=(TP+TN)/total. Error rate=1−accuracy. Precision=TP/(TP+FP). Recall=TP/(TP+FN). F1=2PR/(P+R).
- **Neural network:** input → hidden (ReLU) → output (sigmoid for binary). Loss = binary cross-entropy. Optimizer = Adam. Trained by backpropagation. Epoch = one pass over the data. Dropout prevents overfitting.
- **Normalization/Standardization:** StandardScaler → mean 0, std 1 (fit on train only, then transform test).
- **Gradient descent:** x_new = x − α·f′(x). α = learning rate (too small is slow, too large overshoots). Variants: batch, stochastic, mini-batch.
- **K-Means:** choose K → random centroids → assign points to the nearest centroid → recompute centroids → repeat until stable. **Elbow method:** plot WCSS (inertia) vs K and pick the bend.
- **Hierarchical clustering:** agglomerative (bottom-up), dendrogram, linkage = single/complete/average/ward.
- **Logistic regression:** sigmoid σ(z)=1/(1+e⁻ᶻ) gives a probability; it is a classifier despite the name.
- **Overfitting** (train good, test bad) → fix with more data, regularization, dropout, cross-validation.
