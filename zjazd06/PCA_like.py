import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# 1. Wczytanie i przygotowanie danych
data = load_iris()
X = data.data
y = data.target
feature_names = data.feature_names
labels = data.target_names
colors = ['red', 'green', 'blue']
plt.figure(1)
#plt.scatter(X[:, 0], X[:, 1], c=data.target,label=labels[i])
for i, color in enumerate(colors):
    plt.scatter(X[y == i, 0], X[y == i, 1], c=color, label=labels[i])
plt.xlabel(feature_names[0])
plt.ylabel(feature_names[1])
plt.title(' Iris')
plt.legend()
#plt.colorbar()
#plt.show()
plt.figure(2)
#plt.scatter(X[:, 2], X[:, 3], c=data.target)
for i, color in enumerate(colors):
    plt.scatter(X[y == i, 2], X[y == i, 3], c=color, label=labels[i])
plt.xlabel(feature_names[2])
plt.ylabel(feature_names[3])
plt.title('Iris')
plt.legend()
#plt.colorbar()
plt.show()

# Standaryzacja danych (ważne dla PCA i autoenkoderów)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. Zbudowanie autoenkodera
input_dim = X_scaled.shape[1]  # Liczba cech w danych
encoding_dim = 2  # Wymiar przestrzeni ukrytej (analogicznie do 2 składowych głównych w PCA)

# Warstwa wejściowa
input_layer = Input(shape=(input_dim,))

# Enkoder
encoded = Dense(encoding_dim, activation='relu')(input_layer)

#Dekoder
decoded = Dense(input_dim, activation='sigmoid')(encoded)

# Autoenkoder
autoencoder = Model(input_layer, decoded)

# Enkoder (do redukcji wymiarowości)
encoder = Model(input_layer, encoded)

# 3. Kompilacja i trenowanie modelu
autoencoder.compile(optimizer='adam', loss='mean_squared_error')
#autoencoder.fit(X_scaled, X_scaled, epochs=100, batch_size=16, shuffle=True, verbose=0)
history = autoencoder.fit(X_scaled, X_scaled, epochs=100, batch_size=16, shuffle=True, verbose=0)

loss1 = history.history['loss']
print(f"Wartość funkcji straty po ostatniej epoce: {loss1[-1]}")

# 4. Użycie enkodera do redukcji wymiarowości
X_encoded = encoder.predict(X_scaled)
encoder_weights = autoencoder.layers[1].get_weights()

# 5. Wizualizacja wyników
plt.scatter(X_encoded[:, 0], X_encoded[:, 1], c=y)
for i, color in enumerate(colors):
    plt.scatter(X_encoded[y == i, 0], X_encoded[y == i, 1], c=color, label=labels[i])
plt.xlabel('Pierwsza składowa ukryta')
plt.ylabel('Druga składowa ukryta')
plt.title('Autoenkoder: Redukcja wymiarowości do 2D')
plt.legend()
#plt.colorbar()
plt.show()

plt.plot(history.history['loss'])
plt.title('Historia funkcji straty')
plt.xlabel('Epoka')
plt.ylabel('Strata')
plt.show()

# Wizualizacja macierzy wag
plt.figure(figsize=(8, 4))
sns.heatmap(encoder_weights[0], annot=True, cmap='coolwarm', xticklabels=['Składowa 1', 'Składowa 2'], yticklabels=feature_names)
plt.title('Wagi enkodera')
plt.show()
