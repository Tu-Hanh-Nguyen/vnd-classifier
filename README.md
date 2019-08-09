# Vietnam Dong Classifier

In this project I implement a classifier for the currency of Vietnam, the Vietnam Dong (VND). The idea is a website that foreign people can capture an image of VND note which could be 1k, 2k, 5k, 10k, 20k, 50k, 100k, 200k, and 500k (9 classes), and then the app will recognize the value of the note.

Technical problem to solve:
* How to train a deep learning model to classify the note?
* How to deploy the model in a web application?
* How can a user capture photos on the web?
* How to store the images that users submit?

## Step 1 - Modeling

I followed the fastai course and collect the image of VND on the internet using [Google Image Downloader](https://github.com/hardikvasa/google-images-download) suggested by member of the course.

Then I train a Resnet34 model on Google Colab and have the accuracy of 85%. That was not perfect but good enough to move on the next step which is building the website and deploy the model.

## Step 2 - Taking photo with webcam on browser

I followed this [tutorial](https://www.youtube.com/watch?v=gA_HJMd7uvQ) on Youtube. One thing to be noted was the deprecation of the function `createObjectURL()` in the tutorial. You should use `video.srcObject=stream`.

I improve the UI a bit using [bulma](https://bulma.io/), a free, open source CSS framework (no Javascript).

## Step 3 - Building a Flask app

```
conda create --name currency-classifier python=3.6
conda activate currency-classifier
pip install -r requirements.txt
```

Install Wand problem: it seems like Wand doesn't support imagemagick 7 yet. Install the older version:
```
brew install imagemagick@6
export MAGICK_HOME=/usr/local/opt/imagemagick@6 i
```

I used Filepond for uploading the image to server. All you need to know is in the documentation: https://pqina.nl/filepond/docs/print-version/#filepond-instance


## Part 2

Before you begin, create a new Google Cloud Platform project:
* Sign into [Google Cloud Console](https://console.cloud.google.com/) with your Google Account.
* Click Select a project or the name of your existing project at the top of the page.
* Click New project and follow the prompts on screen.
* Enable Billing. Google Cloud Platform provides $300 credit for new customers, and your usage may be eligible for Google Cloud Platform free-tier. For more information, see [GCP Free Tier](https://cloud.google.com/free/).
* Install [Google Cloud SDK](https://cloud.google.com/sdk/).

Plan:
* Implement authentication
* setup firestore and cloud storage
* build model/image_catalog/ for modeling image in firestore
* setup cloud function to save image into Cloud Storage
* upload image to the cloud function and add new image_id in firestore
* Model in Tensorflow
* Deploy the model
* 
