from sentence_transformers import SentenceTransformer
from pyvi.ViTokenizer import tokenize  # Use this for Vietnamese tokenization
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGController:
    def __init__(self):
        # Load the Vietnamese embedding model from Hugging Face
        self.model = SentenceTransformer('dangvantuan/vietnamese-embedding')

    def embed_text(self, text):
        """
        Embed the text using 'dangvantuan/vietnamese-embedding' model.
        The input text is first tokenized using ViTokenizer, then embedded.
        """
        # Tokenize the text (necessary for Vietnamese language processing)
        tokenized_text = tokenize(text)
        
        # Generate embeddings using the SentenceTransformer model
        embeddings = self.model.encode([tokenized_text])
        return embeddings[0]  # Return the first (and only) embedding

    def rerank_articles(self, question, articles, top_k=5):
        """
        Rerank articles based on their relevance to the question.
        Return the top K most relevant articles.
        """
        # Embed the question (embedding as vector)
        question_embedding = self.embed_text(question)

        # Initialize a list to hold the similarity scores and article data
        ranked_articles = []

        # Loop through each article to calculate similarity with the question
        for article in articles:
            title = article.get('title', 'N/A')
            content = article.get('content', 'N/A')

            # Combine the title and content for better context
            article_text = f"{title}. {content}"
            
            # Embed the article (embedding as vector)
            article_embedding = self.embed_text(article_text)

            # Compute cosine similarity between question and article
            similarity = cosine_similarity(
                question_embedding.reshape(1, -1),
                article_embedding.reshape(1, -1)
            )[0][0]

            # Append the article and its similarity score to the ranked list
            ranked_articles.append((article, similarity))

        # Sort articles by similarity score (highest first)
        ranked_articles.sort(key=lambda x: x[1], reverse=True)

        # Return the top K most relevant articles
        return [article for article, _ in ranked_articles[:top_k]]
