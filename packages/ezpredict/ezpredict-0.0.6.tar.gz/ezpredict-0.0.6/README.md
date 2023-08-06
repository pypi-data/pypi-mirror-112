#### This package is meant to offer a variety of convenient inference functions, particularly for fine-tuned transformers.

Limited to [Jochen Hartmann's](https://github.com/j-hartmann) fine-tuned [j-hartmann/emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) for now.

##### Install:
1. Command line `pip install ezpredict`
2. Google Colab `!pip install ezpredict`


##### Imports:
```
pip install numpy
pip install torch
pip install transformers
```

##### How to use:

```python
from ezpredict import predict

preds = predict.predict_input(model_name="j-hartmann/emotion-english-distilroberta-base",
                             input=["What a beautiful day!"],
                              return_values=True,
                              print_values=True)
``` 
                        
               
                
                
##### Variables: 
 1. `model_name` -> name of model to perform inference on (limited to [Jochen Hartmann's](https://github.com/j-hartmann) fine-tuned [j-hartmann/emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) for now)
 2. `input` -> list of strings to perform predictions on
 3. `return_values` -> True/False, True: returns predictions as list of tuples 
 4. `print_values` -> True/False,  True: returns verbose outputs
 
 
##### Sample output:
```python
[('What a beautiful day!', {'anger': 0.0013013791, 'disgust': 0.00047031444, 'fear': 0.001256481, 'joy': 0.95772415, 'neutral': 0.005870249, 'sadness': 0.004233605, 'surprise': 0.029143812}), ('My grandfather died today.', {'anger': 0.0012322478, 'disgust': 0.002399753, 'fear': 0.0018630251, 'joy': 0.0021994421, 'neutral': 0.012114782, 'sadness': 0.96717805, 'surprise': 0.013012686})]
```





