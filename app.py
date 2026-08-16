from flask import Flask, render_template, request
import os
import urllib.request
import pandas as pd
import joblib

app = Flask(__name__)

# ==========================================================
# LOAD DATA
# ==========================================================
df = pd.read_csv("data/data.csv", encoding="latin1")
products = sorted(df["Description"].dropna().astype(str).unique().tolist())
customers = sorted(df["CustomerID"].dropna().astype(int).unique().tolist())
DEFAULT_CUSTOMER_ID = 17850


# ==========================================================
# LOAD MODELS
# ==========================================================
os.makedirs("models", exist_ok=True)
MODEL_URLS = {
    "models/model_popular.pkl": "https://github.com/ujjwalkumar14b/PickPerfect/releases/download/v1.0.0/model_popular.pkl",
    "models/model_user_item.pkl": "https://github.com/ujjwalkumar14b/PickPerfect/releases/download/v1.0.0/model_user_item.pkl",
    "models/model_cf_user.pkl": "https://github.com/ujjwalkumar14b/PickPerfect/releases/download/v1.0.0/model_cf_user.pkl",
    "models/model_cf_item.pkl": "https://github.com/ujjwalkumar14b/PickPerfect/releases/download/v1.0.0/model_cf_item.pkl",
    "models/model_content.pkl": "https://github.com/ujjwalkumar14b/PickPerfect/releases/download/v1.0.0/model_content.pkl",
    "models/model_hybrid.pkl": "https://github.com/ujjwalkumar14b/PickPerfect/releases/download/v1.0.0/model_hybrid.pkl",
}

# Download any missing model files automatically at startup
for path, url in MODEL_URLS.items():
    if not os.path.exists(path):
        print(f"Downloading {path}...")
        urllib.request.urlretrieve(url, path)
        print(f"Downloaded {path} successfully.")
        
        
model_popular = joblib.load("models/model_popular.pkl")
model_user_item = joblib.load("models/model_user_item.pkl")
model_cf_user = joblib.load("models/model_cf_user.pkl")
model_cf_item = joblib.load("models/model_cf_item.pkl")
model_content = joblib.load("models/model_content.pkl")
model_hybrid = joblib.load("models/model_hybrid.pkl")


# ==========================================================
# PRODUCT DETAILS
# ==========================================================
product_details = {}

for _, row in df.iterrows():
    product = str(row["Product"])
    if product not in product_details:
        product_details[product] = {
            "price": round(float(row["Price"]), 2),
        }


# ==========================================================
# POPULARITY RECOMMENDATION
# ==========================================================
def popularity_recommend(top_n=5):
    return list(model_popular[:top_n])


# ==========================================================
# USER BASED COLLABORATIVE FILTERING
# ==========================================================
def user_based_recommend(customer_id, top_n=5):
    try:
        customer_id = int(customer_id)
        if customer_id not in model_cf_user.index:
            return []

        similar_users = (
            model_cf_user[customer_id]
            .sort_values(ascending=False)
            .iloc[1:6]
            .index
        )

        purchased = model_user_item.loc[customer_id]
        purchased = purchased[purchased > 0].index

        scores = {}

        for user in similar_users:
            items = model_user_item.loc[user]
            for product in items[items > 0].index:
                if product not in purchased:
                    scores[product] = (scores.get(product, 0) + items[product])

        scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [x[0] for x in scores[:top_n]]

    except Exception as e:
        print("User CF Error:", e)
        return []


# ==========================================================
# ITEM BASED COLLABORATIVE FILTERING
# ==========================================================
def item_based_recommend(product_name, top_n=5):
    try:
        if product_name not in model_cf_item.index:
            return []

        recommendations = (
            model_cf_item[product_name]
            .sort_values(ascending=False)
            .iloc[1:top_n + 1]
            .index
            .tolist()
        )
        return recommendations

    except Exception as e:
        print("Item CF Error:", e)
        return []

# CONTENT BASED
def content_recommend(product_name, top_n=5):
    try:
        if product_name not in model_content.index:
            return []

        recommendations = (
            model_content[product_name]
            .sort_values(ascending=False)
            .iloc[1:top_n + 1]
            .index
            .tolist()
        )
        return recommendations

    except Exception as e:
        print("Content Error:", e)
        return []

# HYBRID
def hybrid_recommend(product_name, top_n=5):
    try:
        if (product_name not in model_cf_item.index or product_name not in model_content.index):
            return []

        item_scores = model_cf_item[product_name]
        content_scores = model_content[product_name]
        hybrid_scores = (item_scores * 0.6 + content_scores * 0.4)

        recommendations = (
            hybrid_scores
            .sort_values(ascending=False)
            .iloc[1:top_n + 1]
            .index
            .tolist()
        )
        return recommendations

    except Exception as e:
        print("Hybrid Error:", e)
        return []

# HOME
@app.route("/")
def home():
    return render_template(
        "home.html",
        products=products,
        customers=customers,
        selected_customer=DEFAULT_CUSTOMER_ID,
        selected_product=None,
        popular_recommendations=[],
        user_recommendations=[],
        item_recommendations=[],
        content_recommendations=[],
        hybrid_recommendations=[],
        product_details=product_details
    )

# RECOMMEND
@app.route("/recommend", methods=["POST"])
def recommend():
    selected_product = request.form.get("product")
    
    # Grab selected Customer ID from the form submission
    selected_customer = request.form.get("customer_id", DEFAULT_CUSTOMER_ID)

    popular_recommendations = popularity_recommend()
    user_recommendations = user_based_recommend(selected_customer)
    item_recommendations = item_based_recommend(selected_product)
    content_recommendations = content_recommend(selected_product)
    hybrid_recommendations = hybrid_recommend(selected_product)

    return render_template(
        "recommend.html",
        products=products,
        customers=customers,
        selected_customer=int(selected_customer),
        selected_product=selected_product,
        popular_recommendations=popular_recommendations,
        user_recommendations=user_recommendations,
        item_recommendations=item_recommendations,
        content_recommendations=content_recommendations,
        hybrid_recommendations=hybrid_recommendations,
        product_details=product_details
    )

# RUN
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
