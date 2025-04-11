import os
import wfdb
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

data_path = '/Users/persuren/Downloads/mit-bih-arrhythmia-database-1.0.0/'
record_list = wfdb.get_record_list('mitdb')

rri_data = []
output_labels = []
window_size = 10
for record in record_list:
    annotations = wfdb.rdann(os.path.join(data_path, record), 'atr')
    r_peaks = annotations.sample
    rr_intervals = np.diff(r_peaks)
    normalized_intervals = rr_intervals / np.max(rr_intervals)
    
    for start in range(len(normalized_intervals) - window_size + 1):
        window_symbols = annotations.symbol[start:start + window_size]
        window_features = normalized_intervals[start:start + window_size]
        abnormal_count = sum(1 for symbol in window_symbols if symbol == 'V')
        is_abnormal = abnormal_count >= 2
        is_normal = all(symbol == 'N' for symbol in window_symbols)
        
        if is_normal:
            rri_data.append(window_features)
            output_labels.append(0)
        elif is_abnormal:
            rri_data.append(window_features)
            output_labels.append(1)

X = np.array(rri_data)
y = np.array(output_labels)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

model = Sequential([
    Dense(32, input_dim=window_size, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train_balanced, y_train_balanced, epochs=10, batch_size=64, validation_split=0.2, verbose=1)

def save_trained_model(model, model_path="ekg_model.h5"):
    model.save(model_path)
    print(f"Model kaydedildi: {model_path}")

save_trained_model(model)
