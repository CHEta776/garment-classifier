# Garment Classifier
This repository contain an implementation of a Convolutional Neural Networks for
classifying garments together with a data scraper script, used to download images
from Zalando's online catalogue.

See in depth tutorial on Medium [Automatic Classification of an online Fashion Catalogue: The Simple Way
](https://medium.com/@miguelmndez_30551/automatic-classification-of-an-online-fashion-catalogue-the-simple-way-2a4b13a2af0a)

## Scraper

```
--base_folder         Base folder for downloaded images
--n_images            Number of images to download 
--threads             Number of threads to use
```


#### Run Scraper

```bash
$ python main.py --base_folder='Data/'  --n_images=100 --threads=10
```


## Training

Once the data has been downloaded, the training phase can start. The training file is _train.py_ and receives the following 
parameters:

```
-- learning_rate      Initial learning rate
--epochs              Number of training epochs 
--batch_size          Minibatch training size
--validation_after_n  Number of epochs before apply validation testing
--logdir              Log folder
--save_after_n        Number of epochs before saving network
--model_description   Model name
```

#### Run Train

```bash
$ python train.py --batch_size=512 ---epochs=100 --save_after_n=20 --validation_after_n=5
```


## Evaluation
After training your model with the MNIST fashion data you can check how is it performing
with the data you have downloaded.

```
--model_dir           Saved model directory
--model_description   Model name
--data_path           Images folder path
--batch_size          Minibatch size
```

#### Run Evaluation

```bash
$ python eval.py --batch_size=5 --model_dir='Models/' --model_description='garment_classifier' --data_path='Data/Images'
 --batch_size=5
```

