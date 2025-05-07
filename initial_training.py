import tensorflow as tf
from keras._tf_keras.keras.applications import MobileNetV2
from keras._tf_keras.keras.models import Model
from keras._tf_keras.keras.layers import Dense, GlobalAveragePooling2D
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras._tf_keras.keras.layers import Dropout
from keras._tf_keras.keras import regularizers


image_size = (160, 160)
batch_size = 16

datagen = ImageDataGenerator(
  rescale=1./255,
  validation_split=0.2
)

training_data = datagen.flow_from_directory(
  "data",
  target_size=image_size,
  batch_size=batch_size,
  class_mode='categorical',
  subset='training'
)

validation_data = datagen.flow_from_directory(
  "data",
  target_size=image_size,
  batch_size=batch_size,
  class_mode='categorical',
  subset='validation'
)

print(f"Training data has {len(training_data.filenames)} images in {len(training_data.class_indices)} classes.")
print(f"Validation data has {len(validation_data.filenames)} images in {len(validation_data.class_indices)} classes.")
print("Data loading complete.")

print("Loading MobileNetV2 model...")
base_model = MobileNetV2(input_shape=(*image_size, 3), include_top=False, weights='imagenet')

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01))(x)
x = Dropout(0.5)(x)
output = Dense(4, activation='softmax')(x)

print("Starting training...")
model = Model(inputs=base_model.input, outputs=output)

model.compile(
  optimizer='adam',
  loss='categorical_crossentropy',
  metrics=['accuracy']
)

history = model.fit(
    training_data,
    validation_data=validation_data,
    epochs=5,
    verbose=1
)

# Plot accuracy during training
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

# Plot loss function during training
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

loss, accuracy = model.evaluate(validation_data)
print(f"Model evaluation complete: Loss = {loss:.4f}, Accuracy = {accuracy:.4f}")

model.save("low_vision_minecraft_classifier_test.keras")
print("Model saved as 'low_vision_minecraft_classifier.keras'.")

