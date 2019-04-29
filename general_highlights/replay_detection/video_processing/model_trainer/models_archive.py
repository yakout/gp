"""
This file serves as an archive for the models used in this component.

It makes it easier to roll back to previous models.

Each model's listed here has the best architecture after fine tuning and
hyperparameter tuning.
"""
# Nueral Network Model
NN_model = Sequential()
NN_model.add(Dense(32, input_shape=(self.all_data.shape[1] - 1,), activation='relu'))
NN_model.add(Dense(32, activation='relu'))
NN_model.add(Dense(32, activation='relu'))
NN_model.add(Dense(1, activation='sigmoid'))
NN_model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
# Recurrent Neural Network Model
RNN_model = Sequential()
RNN_model.add(LSTM(20, input_shape=(10, self.all_data.shape[1]), return_sequences=True))
RNN_model.add(TimeDistributed(Dense(1, activation='sigmoid')))
RNN_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
