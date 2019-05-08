"""
This file serves as an archive for the models used in this component.

It makes it easier to roll back to previous models.

Each model's listed here has the best architecture after fine tuning and
hyperparameter tuning.
"""
# Nueral Network Model 78%
model = Sequential()
model.add(Dense(32, input_shape=(self.all_data.shape[1] - 1,), activation='relu'))
model.add(Dense(64, activation='tanh'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='tanh'))
model.add(Dropout(0.4))
model.add(Dense(64, activation='tanh'))
model.add(Dropout(0.6))
model.add(Dense(32, activation='tanh'))
model.add(Dropout(0.6))
model.add(Dense(16, activation='tanh'))
model.add(Dropout(0.2))
model.add(Dense(8, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))# Recurrent Neural Network Model
RNN_model = Sequential()
RNN_model.add(LSTM(20, input_shape=(10, self.all_data.shape[1]), return_sequences=True))
RNN_model.add(TimeDistributed(Dense(1, activation='sigmoid')))
RNN_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
