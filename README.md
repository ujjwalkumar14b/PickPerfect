# PickPerfect - Product Recommendation System

## Overview
This project recommend products based on user preference. It is done by collaborative, content-based, hybrid filtering techniques and popularity techniques.

## Project Structure
```
PickPerfect/
│
├── data/
|   └── cleaned_data.csv
|
├── models/
|   ├── model_cf_item.pkl                           
|   ├── model_cf_user.pkl                          
|   ├── model_content.pkl  
|   ├── model_hybrid.pkl                          
|   ├── model_popular.pkl                           
|   └── model_user_item.pkl 
|
├── static/
├── templates/
│   ├── home.html  
|   └── recommend.html 
|
├── app.py                                      
├── README.md                             
└── Recommendation.ipynb 
```

## Machine Learning Pipeline
- Importing Libraries
- Data Collection 
- Data Preprocessing
- Feature Engineering
- Model Training
- Model Evaluation  
- Model Deploymwent

## Summary

### High User Engagement & Discovery Potential
- 32.13% Hit Rate@5 (Popularity Baseline): Nearly 1 in 3 user sessions displays at least one relevant product within the top 5 recommendations. This high top-of-funnel hit rate drives initial click-throughs, keeps shoppers browsing, and reduces bounce rates.

- 4.77 MAP@5 & 8.68% NDCG@5: The system successfully ranks relevant products near the top of the list, ensuring high-value items get immediate visibility without forcing users to scroll extensively.

### Highly Tailored & Unique User Experiences
- 99.31% Personalization (User CF): The User Collaborative Filtering model delivers exceptionally personalized recommendations across different user segments. This creates a distinct, custom catalog view for each shopper, which builds brand loyalty and improves customer retention.

- 97.98% Personalization (Content-Based): Leveraging product metadata ensures that even when user history is minimal, the system suggests tailored items based on attribute affinity rather than generic defaults.

### Balanced Catalog Exposure & Inventory Health
- 30.79% Catalog Coverage (User CF): The system goes beyond surface-level trending items to actively recommend roughly 31% of your total product inventory.

- Business Impact: Recommending deeper catalog items helps move long-tail inventory, prevents stock stagnation, and reduces over-reliance on a small set of top sellers.

### Areas for Optimization & Growth
- Address Low Precision/Recall (8.23% Precision@5 / 1.75% Recall@5): While the popularity model captures initial interest, precision and recall indicate that users interact with only a fraction of the 5 recommendations presented. Integrating hybrid filtering (combining Content-Based and Collaborative Filtering) can refine these top-5 slots to increase immediate conversion rates and average order value (AOV).

- Cross-Selling & Basket Size: Content-Based Filtering shows promising individual performance (Precision 4.79%, Hit Rate 17.86%). Deploying content-based models on specific product pages as "Frequently Bought Together" or "Similar Items" widgets will capitalize on cross-selling opportunities. 

## Author
Ujjwal Kumar
GitHub: [https://github.com/ujjwalkumar14b](https://github.com/ujjwalkumar14b)
