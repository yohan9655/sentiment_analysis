# sentiment_analysis
Sentiment Analysis using Flair and NLTK
This project uses the Natural Language Toolkit and the Flair toolkit for sentiment analysis.
Articles for the purposes of classification were collected from the URL https://www.aljazeera.com/where/mozambique/.
To run this program first install the dependencies mentioned in the requirements.txt file. All the packages were installed using **conda** with the **conda-forge channel**. Type **conda create --name \<env> --file ./requirements.txt -c condo-forge** to install all the packages.
## Steps to execute
To run the program with given news articles and both flair and nltk type - **python3 driver.py**.
To scrap articles along with the sentiment analysis program type - **python3 driver.py -g true**. To specify the number of articles type **python3 driver.py -g true -n \<number of articles>**. When specifying the number of articles, -g has to be set to true. 
If only nltk or only flair need to be run, then type **python3 driver.py \<name>** and replace \<name> with either nltk or flair.
## Results for 10 articles.
The graph [below](/graphs/fig1.png) shows the result of flair for 10 articles collected from the URL mentioned above.
![](/graphs/fig1.png)
The graph [below](/graphs/fig2.png) shows the results of NLTK for 10 articles collected from the URL mentioned above.
![](/graphs/fig2.png)
The graph [below](/graphs/fig3.png) shows the Subjectivity-Objectivity score of the 10 articles. They were computed using NLTK.
![](/graphs/fig3.png)
