'''
This script contains functions for loading docs (books)
Split them using langchain character text splitter
Create embeddings 
Load them to a vector db - still undecided which to use
'''

import os, time, uuid, fitz
import pandas as pd
import regex as re
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.document_loaders import PyPDFLoader
from vertexai.language_models import TextEmbeddingModel
import vertexai
from vertexai.preview import tokenization
from google.cloud import aiplatform
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv('../.env')
PROJECT_ID = "gen-lang-client-0084223728"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
key_path = os.getenv('GKY')
cred = service_account.Credentials.from_service_account_file(key_path)
vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=cred)
#test - remove below for vertex ai embeddings

#index_endpoints = aiplatform.MatchingEngineIndexEndpoint('projects/713687525028/locations/us-central1/indexEndpoints/8225134226089967616')
text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
#index_endpoints = aiplatform.MatchingEngineIndexEndpoint.list(filter="display_name=physics")
#print(index_endpoints[0])

def generate_text_embedding(text) -> list:
    """Text embedding with a Large Language Model."""
    embeddings = text_embedding_model.get_embeddings([text])
    vector = embeddings[0].values
    return vector

def extractText(d):
	'''
	This function will extract data from the pdf and save it to dataframe
	We could use gemini - but I would rather use it for the core functions
	'''
	pageid = []
	textcontent = []
	tablecontent = []
	pagecontent = []
	src = []
	loader = PyPDFLoader(d, extract_images=False)
	data = loader.load()
	for pages in data:
		textcontent.append(pages.page_content.replace("\n", " "))
		pagecontent.append(pages.metadata)
		pageid.append(pages.metadata['page'])
	df = pd.DataFrame(
		{"page_id": pageid, "page_source": pagecontent, "content": textcontent }
	)

	return df

def splitDocs(dtf):
	'''
	This will split the text content in the extracted data
	input -> dataframe
	'''
	s = []
	loader = DataFrameLoader(dtf, page_content_column="content")
	documents = loader.load()
	text_splitter = RecursiveCharacterTextSplitter(
		separators=["\n", ".", " "],
    	chunk_size=10000, 
    	chunk_overlap=500,
		is_separator_regex=True
	)
	split_book = text_splitter.split_documents(documents)
	for id, split in enumerate(split_book):
		split.metadata['chunk'] = id
	
	num = len(split_book)
	texts = [doc.page_content for doc in split_book]
	text_embeddings_list = []
	id_l = []
	pg_source_list = []
	for doc in split_book:
		id = uuid.uuid4()
		id_l.append(str(id))
		#uncomment and run below when ready to embed and store books to vector stores
		pg_source_list.append(doc.metadata["page_source"])
		text_embeddings_list.append(generate_text_embedding(doc.page_content)) 
		time.sleep(10)
	
	em_df = pd.DataFrame(
		{
			"id": id_l,
			"embedding": text_embeddings_list,
			"page_source": pg_source_list,
			"text": texts
		}
	)
	em_df.to_csv('/Users/vikramsingh/Documents/Projects/genAI/scripts/app/utils/embed_physics.csv', index=False)
	em_df.head()

	return em_df.head()

def countTokens(d):
	model_name = "gemini-1.5-flash-001"
	tokenizer = tokenization.get_tokenizer_for_model(model_name)

	contents = d
	result = tokenizer.count_tokens(contents)
	cost = int(result.total_tokens) * 0.00002
	return result, cost

def createJson(embeddingdtf, unid):
    json_file_name = unid + ".json"
    jsonl_string = embeddingdtf[["id", "embedding"]].to_json(orient="records", lines=True)
    with open(json_file_name, "w") as f:
        f.write(jsonl_string)

    # Show the first few lines of the json file
    #! head -n 3 {json_file_name}
    return json_file_name



def uploadEmbeddings(indx_name,bucket_uri):
	my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    	display_name=f"{indx_name}",
    	contents_delta_uri=bucket_uri,
    	dimensions=768,
    	approximate_neighbors_count=20,
    	distance_measure_type="DOT_PRODUCT_DISTANCE",
	)

def deployIndex(subject,index_name):
    index_endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name='projects/713687525028/locations/us-central1/indexEndpoints/6279579187065913344')
    
    # Initialize the MatchingEngineIndex with the provided index name
    index = aiplatform.MatchingEngineIndex(index_name=f'projects/713687525028/locations/us-central1/indexes/627957918706591334')

    # Generate a unique ID for the deployment
    unique_id = str(uuid.uuid4())

    # Deploy the index
    deployed_index = index_endpoint.deploy_index(
        index=index.resource_name,
        deployed_index_id=f'{subject}_{unique_id}',
        display_name=subject
    )

    return deployed_index

def get_context_from_vertex_ai(subject, question):
    index_endpoints = aiplatform.MatchingEngineIndexEndpoint.list(filter=f"display_name={subject}")
    if not index_endpoints:
            return 'No context - use references and provide accurate answer'

    endpoint_id = '6279579187065913344'
        # Get the first endpoint
    #endpoint = index_endpoints[0]
    endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=endpoint_id)


        # Get the first deployed index
    if not endpoint.deployed_indexes:
        return 'No context - use references and provide accurate answert'
    deployed_index = endpoint.deployed_indexes[0]
    
    query_vector = generate_text_embedding(question)
    
    print(query_vector)
    response = endpoint.find_neighbors(
        deployed_index_id=deployed_index.id,
        queries=[query_vector],
        num_neighbors=5,
		return_full_datapoint=False,
    )
    print(response)
    context = response if response else 'No context provided - use references and provide accurate answers'
    print(deployed_index.id)
    return context

def get_user_token_usage(user_id):
    today = datetime.utcnow().date()
    usage = UserTokenUsage.query.filter_by(user_id=user_id, date=today).first()
    if not usage:
        usage = UserTokenUsage(user_id=user_id, date=today)
        db.session.add(usage)
        db.session.commit()
    return usage

def update_token_usage(user_id, tokens):
    usage = get_user_token_usage(user_id)
    usage.tokens_used += tokens
    db.session.commit()

def check_token_limit(user_id):
    usage = get_user_token_usage(user_id)
    return usage.tokens_used < 100000

def generate_prompt(question, context, subject, lang):
    prompt = f"""
    Context: {context}
    
    Question: {question}
    
    You are a tutor in {subject}. Please provide a comprehensive answer for the question using context.
	If no context - provide a comprehensive answer with references. The answer should be in {lang}
    Answer:
    """
    return prompt

def generate_answer(prompt, model, max_tokens=1000):
    response = model.generate_content(prompt)
    return response.text

def createIndexEndpoint(subject):
	aiplatform.init(project="gen-lang-client-0084223728", location="us-central1")
	my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    	display_name=f"{subject}",
    	public_endpoint_enabled=True,
	)
	return 'Done'
		
def lang_mapping(lang):
	d = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'sw': 'Swahili',
    'zh': 'Chinese',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'ar': 'Arabic',
    'ha': 'Hausa',
    'am': 'Amharic',
    'id': 'Indonesian'
	}
	return d[lang]

if __name__=='__main__':
	#a = extractText('/Users/vikramsingh/Downloads/Physics-WEB_HS.pdf')
	#b = splitDocs(a)
	#c = countTokens(b)
	#d = createJson(b,'physics')
	#d = uploadEmbeddings('physics','gs://phrashnai_bucket/physics.json')
	#d = createIndexEndpoint('physics')
	#d = deployIndex('physics','')
	print('Done')
	
