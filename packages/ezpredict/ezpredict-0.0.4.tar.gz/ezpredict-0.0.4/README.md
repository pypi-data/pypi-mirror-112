This package is meant to offer a variety of convenient inference functions, particularly for fine-tuned transformers.
Limited to j-hartmann's fine-tuned emotion-english-distilroberta-base -> https://huggingface.co/j-hartmann/emotion-english-distilroberta-base for now.


Installs:
pip install numpy
pip install torch
pip install transformers

How to use:

from ezpredict import predict

preds = predict.predict_input(model_name="j-hartmann/emotion-english-distilroberta-base",
              input=["What a beautiful day!" , "The universe is a function build to evovle increasingly intelligent neural networks."],
               return_values=True,
                print_values=True)
                
Where:
 model_name -> name of model to perform inference on (limited to "j-hartmann/emotion-english-distilroberta-base" for now)
 input -> list of strings to perform predictions on
 return_values -> True/False, True: returns predictions as list of tuples 
 print_values -> True/False,  True: returns verbose outputs


