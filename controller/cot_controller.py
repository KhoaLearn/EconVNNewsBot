from openai import OpenAI
import os
from dotenv import load_dotenv
from controller.rag_controller import RAGController  # Import RAGController for reranking articles

# Load environment variables from .env file
load_dotenv()

class CoTController:
    def __init__(self):
        # Initialize OpenAI API with API key from environment
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.rag_controller = RAGController()  # Initialize RAGController for reranking articles

    def analyze_chunk(self, chunk, question):
        """
        Analyze a single chunk of an article related to the question.
        """
        title = chunk.get('title', 'N/A')
        source = chunk.get('source', 'N/A')
        url = chunk.get('url', 'N/A')
        category = chunk.get('category', 'N/A')
        chunk_id = chunk.get('chunk_id', 'N/A')
        content = chunk.get('content', 'N/A')[:700]  # Limit content to first 700 characters
        published_date = chunk.get('published_date', 'N/A')

        # Create a prompt to analyze the chunk with specific instructions to avoid hallucination
        # prompt_chunk = f"""
        # Analyze the following article published on {published_date} with title '{title}' :
        
        # Content: {content}

        # How does this chunk help answer the question: '{question}'?

        # Focus on the economic context and important details mentioned in the chunk. Please ensure the analysis is accurate and relevant to the publication date. If there is no relevant information to answer the question '{question}', please return 'no relevant information' from {source}. Do not add any information that is not present in the chunk content.
        # """
        prompt_chunk = f"""
        Step-by-Step Analysis:

        1. **Identify Key Information**: Based on the content provided below, identify the main points related to the query '{question}'.
        
        Content: "{content}"
        
        2. **Economic Relevance**: Evaluate how this information is relevant to the economic context of the question, with attention to any details about infrastructure, foreign investments, market trends, or economic recovery.

        3. **Answer Contribution**: Explain how this chunk contributes to answering the question '{question}'. If there is no relevant information in this chunk, please respond with 'no relevant information' and specify the source as {source}.

        Note: Ensure that the analysis is accurate, relevant to the publication date ({published_date}), and avoid adding any information not present in the content.
        """
        
        # Call OpenAI API to generate the analysis
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in Vietnamese economic news analysis. Please provide detailed and precise answers based on the information provided."},
                {"role": "user", "content": prompt_chunk}
            ],
            max_tokens=300,
            temperature=0.5
        )

        # Extract the content from the API response
        analysis = response.choices[0].message.content

        # Return the analysis with citation info
        return analysis

    def generate_chain_of_thoughts(self, articles, question):
        """
        Generate the final answer based on analyzing multiple articles using Chain of Thought.
        Consolidate chunks with the same title into a single citation.
        First rerank the articles using RAGController, then process only the top-ranked articles.
        """
        # Rerank the articles using RAGController and get the top articles
        # top_articles = self.rag_controller.rerank_articles(question, articles, top_k=5)
        # Rerank the articles using RAGController and get the top articles
        top_articles = self.rag_controller.rerank_articles(question, articles, top_k=5)


        chain_of_thoughts = ""
        cite_list = []  # To store the list of unique references
        citation_tracker = set()  # Track unique articles by title and date

        for article in top_articles:
            title = article.get('title', 'N/A')
            published_date = article.get('published_date', 'N/A')
            source = article.get('source', 'N/A')
            
            # Analyze each chunk
            analysis = self.analyze_chunk(article, question)
            chain_of_thoughts += analysis

            # Add to citation list if the title + published_date hasn't been added before
            citation_key = (title, published_date)
            if citation_key not in citation_tracker:
                cite_list.append({
                    'title': title,
                    'source': source,
                    'published_date': published_date,
                    'url': article.get('url', 'N/A')
                })
                citation_tracker.add(citation_key)  # Mark as cited

        # Combine the analyses and answer the question
        # final_prompt = f"Based on the following analyses of multiple articles:\n\n{chain_of_thoughts}\n"
        # final_prompt += f"Please synthesize the information and answer the following question: '{question}'.\n"
        # final_prompt += "Ensure the answer is based on the combined analyses and cite the relevant articles using their publication dates and titles. If there is no relevant information to answer the question '{question}', please return 'Curently we have no relevant information' from {source}. Do not add any information that is not present in the article content."
        # final_prompt += " The answer should be in Vietnamese."
        final_prompt = f"""
        Based on the following step-by-step analyses of multiple articles:

        {chain_of_thoughts}

        Please synthesize the information and answer the question: '{question}'.

        Steps for Synthesis:
        1. Summarize the key points from each analysis that are relevant to the question.
        2. Identify any recurring themes or important economic indicators mentioned across the articles.
        3. Provide a coherent answer that combines these insights, ensuring it is contextually relevant and accurate.
        4. Cite the relevant articles by their titles and publication dates. If there is no relevant information to answer the question, please respond with 'Currently we have no relevant information' and specify the source. Avoid adding any information not present in the article content.

        Note: The answer should be in Vietnamese.
        """
        
        
        # Call OpenAI API to generate the final answer
        final_response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in Vietnamese economic news analysis. Please provide detailed and precise answers based on the information provided."},
                {"role": "user", "content": final_prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )

        # Extract the final answer from the API response
        final_answer = final_response.choices[0].message.content
        return final_answer, cite_list
