**Note:** currently moving to a blueprint style Flask system so some features may be missing/incompatible temporarily.
# Project: Libera
Project: Libera is an intelligent user content connector I created as my passion project at Metis' Data Science Bootcamp in Chicago. Project: Libera uses a custom designed webcrawler to automatically seek out web content related to the field of Data Science and collect relevant posts on MongoDB. These posts are then subtopiced using NMF based topic modelling and an agglomerative clustering model. The front end allows users to register an account and declare interests from 10 subtopics after which they are provided with web content recommendations based on their selected interests. The recommendations feed allows users to like, dislike, flag, and move through content naturally and uses Embedly cards to provide snapshots of recommended posts.  
  
**Tools Used:** BS4, MongoDB, SQL, SKLearn (Naive Bayes Classification, NMF, Agglomerative Clustering), NLP, Flask, MatPlotLib, Seaborn, Pandas.  
  
**Demo video:** https://drive.google.com/open?id=0B1wKwsg7SD6sV0JKQXJzUURlcjA  
  
## Pipeline  
1. Collection of Data - [Web Crawler](https://github.com/paulfblack/project_libera/blob/master/libera_notebooks/Web_Crawler.ipynb)  
  a. Hand Classification - [Libera Quick Rate](https://github.com/paulfblack/project_libera/tree/master/libera_quick_rate/libera_quick_rate)  
  b. [Tokenization](https://github.com/paulfblack/project_libera/blob/master/libera_notebooks/libera_tokenization.py)  
  c. [Naive Bayes Classification Model](https://github.com/paulfblack/project_libera/blob/master/libera_notebooks/naive_bayes.ipynb) 
2. [Subtopicing and Agglomerative Clustering](https://github.com/paulfblack/project_libera/blob/master/libera_notebooks/topic_modelling_agglomerative_clustering.ipynb) 
3. Distribution - [Flask App](https://github.com/paulfblack/project_libera/tree/master/libera)  
  
## Designing Project: Libera
<img src="https://github.com/paulfblack/project_libera/blob/master/Images/logo.png" alt="Libera Logo" align="middle" height=250px>  
  
Project: Libera was designed to automate the process of collecting new information. The driving concept behind Project: Libera is that the informational ecosystem we live in today is much like a labyrinth: constantly shifting and changing. In order to stay relevant in this intellectual labyrinth, one must constantly seek out new information and manually seeking out information or relying on a pre-existing social network isn't always enough. Project: Libera was designed to bridge this gap between user and content. Flexible design allows for the inclusion of new topics other than data science with ease, meaning that, whatever your interests Project: Libera can connect you with relevant content. Project: Libera, your guide through the labyrinth.  
  
## Custom Webcrawler  
At the core of Project: Libera is a custom designed [web crawler](https://github.com/paulfblack/project_libera/blob/master/libera_notebooks/Web_Crawler.ipynb) which uses Beautiful Soup, Requests, NLP, Regular Expressions, and PyMongo to seek out new web content and store relevant content remotely. By running the web crawler on Amazon Web Services, it can continue to collect information around the clock. The web crawler takes  "seed blogs" related to data science and visits all of the pages those seeds directly link to and determines if they are relevant or not. Relevant blogs are stored remotely and flagged as "open_seed" for future use. When calling the function to run the web crawler, you can determine a max number of seeds used to prevent it from running indefinitely. When the web crawler terminates, it sends out an e-mail using SMTPLib to notify the user so you don't have to constantly check the AWS instance.  
  
### Initializing a Topic  
Project: Libera's web crawler uses a Naive Bayes classification model to determine if a new post is related to the topic of interest. When initializing on a new topic it is important that this or some other classification model is trained, otherwise the web crawler is useless. This requires a labelled dataset of web content that represents both related and unrelated posts. To gather data, I turned off the quality_check function on the web crawler by commenting out its content and adding return True. This allows the webcrawler to randomly pull all text it encounters. I then fed it 200 seed blogs that were related to data science that I hand picked. From here it visited every page that these seeds directly linked to and pulled their content, ending with 4,000 posts.  
  
### Hand Classifying Posts  
Having 4,000 posts is not enough to train a model, they need to be classified as related or unrelated as well. Even though in the grand scheme of things 4,000 posts is rather small, hand classifying these would be rather time consuming. The [libera_quick_rate](https://github.com/paulfblack/project_libera/tree/master/libera_quick_rate/libera_quick_rate) Flask app pulls blogs from MongoDB one at a time and displays their URL and their text content. The WASD and up, left, down, right keys are key bound to allow for quick classification (W and up = undo, A and left = mark as unrelated, S and Down = skip, D and right = mark as related). With this system I was able to hand classify the 4,000 posts in a day from which a Naive Bayes model could be trained.  
  
### Training the Naive Bayes Model  
Naive Bayes works well with unbalanced classes and high dimensional spaces and performed well for Project: Libera's needs. The goal was to optimize precision in relevant classes so that the posts that made it into the database were unlikely to be irrelevant to data science. I found that transforming the text documents with a count vectorizer (max features = 3000) and then transforming that with a tf-idf transformer worked best, but this is data dependant.  
  
## Topic Modelling and Agglomerative Clustering  
With the classification model trained and the web crawler up and running, I moved on to subtopicing data science. Non-negative Matrix Factorization gave me the clearest topic spaces at around 10 dimensions. Increasing the dimensions showed promise of reducing algorithms into splits such as supervised and unsupervised and at very high dimensional spaces specific algorithms became topics. This came at the cost of having topic dimensions that seemed meaningless and was too subdivided for my taste so I currently have 10.  
  
In this new topic space, I fit an agglomerative clustering model (SKLearn) onto the data and then looked at the average topic breakdown by cluster. It worked out that the number of clusters fit the number of topics here (with 10 having the highest sillhouette score), but I am curious to see if this changes as new data is incorporated and models are refit. Cosine distance was used so that length differences in blog posts would not create new clusters.  
  
## Front End  
Project: Libera's front end is a Flask based web app where users can register an account, declare their interests and receive tailored recommendations based on these interests. The web crawler is designed to accumulate the number of external links pointing to each blog post allowing for the implementation of a page rank system. As this is still early in development, the first pass at a page rank system was perhaps too naive so it has temporarily been removed while I rework the design. The allowance for user feedback also lends itself to the potential inclusion of collaborative filtering, something I hope to add in the future.  
  
Thank you for taking the time to read about Project: Libera for more information or questions feel free to reach out to me via e-mail, paul.laifu.black@gmail.com
