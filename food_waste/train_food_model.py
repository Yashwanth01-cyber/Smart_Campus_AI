import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.callbacks import ModelCheckpoint

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")  # Should contain 'full/' and 'empty/' subfolders
MODEL_FILE = os.path.join(BASE_DIR, "food_model.h5")

# Check dataset
if not os.path.exists(DATASET_DIR):
    raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

classes = sorted([d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))])
print("Classes found:", classes)

# -------------------------
# Data Augmentation
# -------------------------
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(128,128),
    batch_size=16,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(128,128),
    batch_size=16,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

# -------------------------
# Build CNN Model
# -------------------------
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(classes), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# -------------------------
# Train Model
# -------------------------
checkpoint = ModelCheckpoint(MODEL_FILE, monitor='val_accuracy', save_best_only=True, verbose=1)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=15,
    callbacks=[checkpoint]
)

print(f"Training complete! Model saved as: {MODEL_FILE}")
