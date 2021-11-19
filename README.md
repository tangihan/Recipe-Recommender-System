**Healthy Recipe Recommender System**
-
We explored 2 types of recommender systems to recommend Top N healthy and tasty recipes. 

Approach 1: Content-Based Filtering
-
In this approach, we used the features of the recipes to recommend users based on the recipes he or she has previously reacted positively to. Using Natural Language Processing (NLP), we performed BERTopic and Latent Dirichlet Allocation (LDA) Topic Modelling on the descriptions and names of the recipes to extract features. Other features that were included in the model are the minutes for preparing the recipes, number of ingredients required and category of the recipe.  

To extract the user's preference, we used the top 3 topics based on the occurrence among the recipes that were rated 5 by the user.

Approach 2: Item-based Collaborative Filtering
-
Approach 2 leverages on the historical rating of recipes as features. In this approach, it is assumed that the users will like recipes similar to what they had liked previously as well as recipes that are liked by other users that have similar tastes. 

To extract the user's preferences, we used recipes that were previously rated 5 by the user.

Additional Feature: Health Rank
-
To assign health rank to the recipes, we used Gaussian Mixture intialised with K-means to cluster the recipes based on the nutrients of interest for each category of recipes. The nutrients of interest are obtained from Singapore's Health Promotion Board guidelines. After that, we manually grouped the results into their respective health rank based on the median Percentage Daily Values (PDV) of each cluster. For each category, the recipes are grouped into 3 groups: Rank 1 represents most healthy, Rank 2 represents moderately healthy and Rank 3 represents least healthy. 

The health rank is then used to sort the recommended recipes before recommending Top N recipes to the user. 

