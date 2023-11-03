import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from keras.models import Model
from keras.layers import Input, Dense
from keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder
class model:
    # Load the dataset
    df = pd.read_csv('Final.csv')

    # Extract the 'Question' and 'Code' columns from the dataset
    questions = df['Question'].values.tolist()
    codes = df['Code'].values.tolist()

    # Encode the codes into integers
    label_encoder = LabelEncoder()
    encoded_codes = label_encoder.fit_transform(codes)

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(questions)

    # Convert sparse matrix to dense array
    tfidf_matrix = tfidf_matrix.toarray()

    # Define the DEC model architecture
    input_dim = tfidf_matrix.shape[1]
    latent_dim = 45

    input_layer = Input(shape=(input_dim,))
    encoder = Dense(latent_dim, activation='relu')(input_layer)
    decoder = Dense(input_dim, activation='sigmoid')(encoder)
    autoencoder = Model(inputs=input_layer, outputs=decoder)

    # Define the clustering layer
    num_clusters = len(np.unique(encoded_codes))
    clustering_layer = Dense(num_clusters, activation='softmax')(encoder)
    clustering_model = Model(inputs=input_layer, outputs=clustering_layer)

    # Compile the clustering model
    clustering_model.compile(optimizer=Adam(learning_rate = 0.001), loss='categorical_crossentropy')

    # Convert labels to one-hot encoding
    one_hot_labels = pd.get_dummies(encoded_codes).values

    # Train the clustering model
    clustering_model.fit(tfidf_matrix, one_hot_labels, batch_size=5, epochs=6)

    new_question = "Pandas and Numpy"
    new_question_vector = vectorizer.transform([new_question])
    new_question_vector = new_question_vector.toarray()
    cluster_probs = clustering_model.predict(new_question_vector)
    predicted_cluster = np.argmax(cluster_probs)

    # Decode the predicted cluster back to the original code
    code = label_encoder.inverse_transform([predicted_cluster])[0]

    # Print the corresponding code
    # print("Predicted Code:", code)
    questions_with_code = df[df['Code'] == code]['Question'].values
    # print("Questions with the predicted code:")
    # for question in questions_with_code:
    #     print(question)