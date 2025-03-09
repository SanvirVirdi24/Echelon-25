import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import joblib

class ClothingRecommender:
    def __init__(self, data_path=None, df=None):
        """
        Initialize the recommender system with either a file path or dataframe
        
        Parameters:
        data_path (str): Path to the CSV file containing clothing data
        df (pandas.DataFrame): DataFrame containing clothing data
        """
        if df is not None:
            self.df = df
        elif data_path:
            self.df = pd.read_csv(data_path)
        else:
            raise ValueError("Either data_path or df must be provided")
            
        # Clean the dataframe
        self.df = self.df.dropna()
        
        # Create user-item matrix for collaborative filtering
        self.user_item_df = self.create_user_item_matrix()
        
        # Model containers
        self.content_based_model = None
        self.cf_model = None
        self.feature_matrix = None
        self.encoder = None
        self.scaler = None
        
    def create_user_item_matrix(self):
        """Create a user-item matrix for collaborative filtering"""
        # For each user, get their order amount for each product category
        user_item = self.df.pivot_table(
            index='Customer_ID', 
            columns='Product_Category', 
            values='Order_Amount', 
            aggfunc='sum',
            fill_value=0
        )
        return user_item
    
    def train_content_based(self):
        """Train a content-based recommendation model"""
        # Select features for content-based filtering
        categorical_features = ['Product_Category', 'Payment_Method', 'Device_Used']
        
        # Create encoder for categorical features
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        
        # Prepare the data
        content_df = self.df.drop_duplicates(subset=['Product_ID'])
        
        # Extract categorical features
        cat_data = content_df[categorical_features]
        encoded_features = self.encoder.fit_transform(cat_data)
        
        # Extract numerical features
        numerical_features = ['Order_Amount', 'Discount_Applied', 'Browsing_Time']
        num_data = content_df[numerical_features].values
        
        # Scale numerical features
        self.scaler = StandardScaler()
        scaled_num_data = self.scaler.fit_transform(num_data)
        
        # Combine features
        self.feature_matrix = np.hstack((encoded_features, scaled_num_data))
        
        # Calculate similarity matrix
        self.content_based_model = cosine_similarity(self.feature_matrix)
        
        return self
    
    def train_collaborative_filtering(self):
        """Train a collaborative filtering model using SVD"""
        # Prepare data for Surprise
        reader = Reader(rating_scale=(0, self.df['Order_Amount'].max()))
        
        # Create dataset from dataframe
        data = Dataset.load_from_df(
            self.df[['Customer_ID', 'Product_ID', 'Order_Amount']], 
            reader
        )
        
        # Split data for training
        trainset, _ = train_test_split(data, test_size=0.2)
        
        # Train model
        self.cf_model = SVD()
        self.cf_model.fit(trainset)
        
        return self
    
    def get_content_based_recommendations(self, product_id, n=5):
        """
        Get content-based recommendations for a product
        
        Parameters:
        product_id (str): ID of the product to get recommendations for
        n (int): Number of recommendations to return
        
        Returns:
        list: List of product IDs recommended
        """
        if self.content_based_model is None:
            self.train_content_based()
            
        # Get the index of the product
        products = self.df.drop_duplicates(subset=['Product_ID'])
        product_indices = {id: idx for idx, id in enumerate(products['Product_ID'])}
        
        if product_id not in product_indices:
            return []
            
        idx = product_indices[product_id]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.content_based_model[idx]))
        
        # Sort based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top n similar products
        sim_scores = sim_scores[1:n+1]
        product_indices = [i[0] for i in sim_scores]
        
        # Return product IDs
        recommended_products = products.iloc[product_indices]['Product_ID'].tolist()
        
        return recommended_products
    
    def get_collaborative_recommendations(self, user_id, n=5):
        """
        Get collaborative filtering recommendations for a user
        
        Parameters:
        user_id (str): ID of the user to get recommendations for
        n (int): Number of recommendations to return
        
        Returns:
        list: List of product IDs recommended
        """
        if self.cf_model is None:
            self.train_collaborative_filtering()
            
        # Get all products
        all_products = self.df['Product_ID'].unique()
        
        # Get products the user has already interacted with
        user_products = self.df[self.df['Customer_ID'] == user_id]['Product_ID'].unique()
        
        # Find products the user hasn't interacted with
        new_products = np.setdiff1d(all_products, user_products)
        
        # If the user has interacted with all products, return empty list
        if len(new_products) == 0:
            return []
            
        # Get predictions for all new products
        predictions = []
        for product_id in new_products:
            prediction = self.cf_model.predict(user_id, product_id)
            predictions.append((product_id, prediction.est))
            
        # Sort by predicted rating
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Return top n product IDs
        return [p[0] for p in predictions[:n]]
    
    def get_hybrid_recommendations(self, user_id, product_id=None, n=5):
        """
        Get hybrid recommendations combining content-based and collaborative filtering
        
        Parameters:
        user_id (str): ID of the user to get recommendations for
        product_id (str, optional): ID of a product to base recommendations on
        n (int): Number of recommendations to return
        
        Returns:
        list: List of product IDs recommended
        """
        # Get collaborative filtering recommendations
        cf_recs = self.get_collaborative_recommendations(user_id, n=n)
        
        # If product_id is provided, get content-based recommendations
        if product_id:
            cb_recs = self.get_content_based_recommendations(product_id, n=n)
            
            # Combine recommendations (simple approach: alternate between the two lists)
            hybrid_recs = []
            for i in range(min(n, max(len(cf_recs), len(cb_recs)))):
                if i < len(cf_recs):
                    hybrid_recs.append(cf_recs[i])
                if i < len(cb_recs):
                    if cb_recs[i] not in hybrid_recs:  # Avoid duplicates
                        hybrid_recs.append(cb_recs[i])
                        
            return hybrid_recs[:n]
        else:
            return cf_recs[:n]
    
    def get_category_recommendations(self, category, n=5):
        """
        Get recommendations for a specific product category
        
        Parameters:
        category (str): Product category
        n (int): Number of recommendations to return
        
        Returns:
        list: List of product IDs recommended
        """
        # Get products in the category
        category_products = self.df[self.df['Product_Category'] == category]
        
        # Sort by popularity (number of orders)
        product_popularity = category_products.groupby('Product_ID').size().reset_index(name='count')
        product_popularity = product_popularity.sort_values('count', ascending=False)
        
        # Return top n products
        return product_popularity.head(n)['Product_ID'].tolist()
    
    def get_popular_recommendations(self, n=5):
        """
        Get recommendations based on overall popularity
        
        Parameters:
        n (int): Number of recommendations to return
        
        Returns:
        list: List of product IDs recommended
        """
        # Calculate product popularity
        product_popularity = self.df.groupby('Product_ID').size().reset_index(name='count')
        product_popularity = product_popularity.sort_values('count', ascending=False)
        
        # Return top n products
        return product_popularity.head(n)['Product_ID'].tolist()
    
    def get_recommendations_for_new_users(self, n=5):
        """
        Get recommendations for new users with no history
        
        Parameters:
        n (int): Number of recommendations to return
        
        Returns:
        list: List of product IDs recommended
        """
        # Return popular products
        return self.get_popular_recommendations(n)
    
    def save_model(self, filepath):
        """Save the model to a file"""
        model_data = {
            'content_based_model': self.content_based_model,
            'cf_model': self.cf_model,
            'feature_matrix': self.feature_matrix,
            'encoder': self.encoder,
            'scaler': self.scaler
        }
        joblib.dump(model_data, filepath)
        
    def load_model(self, filepath):
        """Load the model from a file"""
        model_data = joblib.load(filepath)
        self.content_based_model = model_data['content_based_model']
        self.cf_model = model_data['cf_model']
        self.feature_matrix = model_data['feature_matrix']
        self.encoder = model_data['encoder']
        self.scaler = model_data['scaler']
        
        return self

# Example of how to use the recommendation system
if __name__ == "__main__":
    # Initialize the recommender with your CSV file
    recommender = ClothingRecommender("clothing_dataset.csv")
    
    # Train the models
    recommender.train_content_based()
    recommender.train_collaborative_filtering()
    
    # Get recommendations for a user
    user_id = "ae480c1c-9745-4d76-93ac-346ef28ddb26"
    recommendations = recommender.get_hybrid_recommendations(user_id, n=5)
    
    print(f"Recommended products for user {user_id}: {recommendations}")
    
    # Get recommendations based on a product
    product_id = "d5e29dd8-9f1d-4f50-86c4-75a01c459f76"
    recommendations = recommender.get_content_based_recommendations(product_id, n=5)
    
    print(f"Similar products to {product_id}: {recommendations}")
    
    # Save the model
    recommender.save_model("clothing_recommender_model.pkl")