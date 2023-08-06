# author: Samuel Domdey

# Install the transformers library
import torch
import numpy as np 
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# model_name: give name of pretrained model you want to load and use for inference
# input: give list of sentences you want to have analysed
def predict_input(model_name, input, return_values, print_values):

    # define tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # load pretrained model
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Obtain emotion probabilities (sorted)
    emotion_labels = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']


     # create datastructures if True
    if return_values == True:
        emo_dict = {emo: None for emo in emotion_labels}
        predictions = []

        # iterate over given list of sentences
        for index, value in enumerate(input):

            # Tokenize texts and create prediction data set, truncate long inputs, give padding to inputs
            tokenized_texts = tokenizer(value, truncation=True, padding=True, return_tensors="pt")

            # Prediction
            # tensor ([1]) -> tensor([[1]])
            labels = torch.tensor([1]).unsqueeze(0)
            outputs = model(**tokenized_texts, labels=labels)
            loss, logits = outputs[:2]
            # tensor ([[]]) -> tensor ([])
            logits = logits.squeeze(0)

            # Probabilities
            # perform softmax on logits
            probabilities_tensor = torch.nn.functional.softmax(logits, dim=0)

            # detaches tensor from graph, convert to numpy array
            probabilities_numpy = np.array(probabilities_tensor.detach().numpy())



            # sort np-array by values low-high, flip to high-low
            emotion_values = np.argsort(probabilities_numpy)[::-1]

            print("Prediction for input:", value)
            # Print emotion labels with respective prediction values
            for emotion in range(len(probabilities_numpy)):
                # current emotion
                em = emotion_labels[emotion_values[emotion]]
                # current probability
                prob = probabilities_numpy[emotion_values[emotion]]

                emo_dict[em] = prob

                if print_values == True:
                    print(f"{em}:\n" + f"{np.round(float(prob), 10)}\n")

            if print_values == True:
                print("\n")

            predictions.append((value, emo_dict.copy()))

        # return data if True
        return predictions


    # if datastructure to be returned
    else:

        # iterate over given list of sentences
        for index, value in enumerate(input):

            # Tokenize texts and create prediction data set, truncate long inputs, give padding to inputs
            tokenized_texts = tokenizer(value, truncation=True, padding=True, return_tensors="pt")

            # Prediction
            # tensor ([1]) -> tensor([[1]])
            labels = torch.tensor([1]).unsqueeze(0)
            outputs = model(**tokenized_texts, labels=labels)
            loss, logits = outputs[:2]
            # tensor ([[]]) -> tensor ([])
            logits = logits.squeeze(0)

            # Probabilities
            # perform softmax on logits
            probabilities_tensor = torch.nn.functional.softmax(logits, dim=0)

            # detaches tensor from graph, convert to numpy array
            probabilities_numpy = np.array(probabilities_tensor.detach().numpy())

            # sort np-array by values low-high, flip to high-low
            emotion_values = np.argsort(probabilities_numpy)[::-1]

            if print_values == True:
                print("Prediction for input:", value)
            # Print emotion labels with respective prediction values
            for emotion in range(len(probabilities_numpy)):
                # current emotion
                em = emotion_labels[emotion_values[emotion]]
                # current probability
                prob = probabilities_numpy[emotion_values[emotion]]

                if print_values == True:
                    print(f"{em}:\n" + f"{np.round(float(prob), 10)}\n")
            if print_values == True:
                print("\n")


