# Import Library
import tensorflow
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense, Dropout, concatenate


# Fit modelo no dataset
def fit_model(x_train, y_train, n_features=23):
    model = Sequential()
    # Initial layer
    model.add(Dense(units=100, input_shape=(n_features,), activation='relu'))
    model.add(Dropout(0.2))
    # Hidden layer
    model.add(Dense(units=100, activation='relu'))
    model.add(Dropout(0.2))
    # Hidden layer
    model.add(Dense(units=n_features, activation='relu'))
    # Output layer
    model.add(Dense(units=3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit model
    model.fit(x_train, y_train, epochs=500, verbose=0)

    return model


def load_all_models_members(n_models, n_features=23):
    all_models = []
    for i in range(n_models):
        model = Sequential()
        # Initial layer
        model.add(Dense(units=100, input_shape=(n_features,), activation='relu'))
        model.add(Dropout(0.2))
        # Hidden layer
        model.add(Dense(units=100, activation='relu'))
        model.add(Dropout(0.2))
        # Hidden layer
        model.add(Dense(units=n_features, activation='relu'))
        # Output layer
        model.add(Dense(3, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Define filename for this ensemble
        try:
            filename = 'model\\modelo_rede_especialista_{}.h5'.format(i+1)
            model.load_weights(filename)
        except Exception as e:
            ds_msg_error = 'ERRO AO CARREGAR O MODELO ESPECIALISTA'
            ds_error = msg_exception('Error: {}'.format(e))
            ds_method = 'load_all_models_members'
            insert_msg_error('', ds_msg_error, ds_error, ds_method)

        # Add to list of members
        all_models.append(model)

    return all_models


# Defines the final model using the members' models as input
def define_decisor_model(members):
    # Blocks all layers on all models from being trained
    for model in members:
        for layer in model.layers:
            # Make not trainable
            layer.trainable = False
            # Rename to avoid 'unique layer name' issue
            # layer.name = 'ensemble_' + str(i+1) + '_' + layer.name
    # Define multi-headed input
    ensemble_visible = [model.input for model in members]
    # Concatenate merge output from each model
    ensemble_outputs = [model.output for model in members]
    merge = concatenate(ensemble_outputs)
    hidden = Dense(100, activation='relu')(merge)
    output = Dense(3, activation='softmax')(hidden)
    model = Model(inputs=ensemble_visible, outputs=output)
    # model.summary()
    # Plot graph of ensemble
    # plot_model(model, show_shapes=True, to_file='model_graph.png')
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


# Fit the final model
def fit_decisor_model(model, X_input, Y_input):
    # Prepare input data
    X = [X_input for _ in range(len(model.input))]
    # Encode output data
    Y_input_cat = to_categorical(Y_input)
    # Fit model
    model.fit(X, Y_input_cat, epochs=100, verbose=0)

    return model


# Make a prediction with a stacked model
def predict_decisor_model(model, X_input):
    # Prepare input data
    X = [X_input for _ in range(len(model.input))]
    # Make prediction
    return model.predict(X, verbose=0)
