from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import CacheBackedEmbeddings
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings, CacheBackedEmbeddings
#from langchain_google_vertexai import VertexAI
import tiktoken
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser

load_dotenv('/Users/vikramsingh/Documents/Projects/genAI/scripts/.env')
ky = os.getenv('KY')
pdf_file_name = '/Users/vikramsingh/Downloads/Travel_Letter.pdf'
pdf_folder_path = 'Users/vikramsingh/Downloads'
#genai.configure(api_key=ky)
#model = genai.GenerativeModel('gemini-1.5-flash')
lm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=ky,max_output_tokens=1000,temperature=0)

def load_pdf(directory, file):
	loader = PyPDFLoader(file, extract_images=False)
	data = loader.load()
	txt = []
	for pages in data:
		txt.append(pages.page_content)
	return "\n".join(txt)

def splitText(data):
	text_splitter = RecursiveCharacterTextSplitter(
    	separators=["\n", ".", " "],
    	chunk_size=1000, 
    	chunk_overlap=20,
		is_separator_regex=True
	)
	d = text_splitter.split_text(str(data))
	return d

def summarizeData(data, mo):
	#chain = load_summarize_chain(mo, chain_type="stuff")
	#a = chain.run(data)
	#return a
	pt = """You are an assistant tasked with explaining text from documents. \
    These explanations will be embedded and used for retrieval. \
    Give a detailed explanation of the text. Text: {element} """
	prompt = PromptTemplate.from_template(pt)
	model = LLMChain(llm=mo,prompt=prompt)
	text_summaries = []
	summarize_chain = {"element": lambda x: x} | prompt | model 
	summaries = summarize_chain.batch(data, {"max_concurrency": 1})
	text_summaries = [summary['text'] for summary in summaries]	
	#return text_summaries

	#text_summaries = summarize_chain.batch(data, {"max_concurrency": 1})
	#text_summaries = stuff_chain.run(data)
	
	#text_summaries = summarize_chain.batch(data, {"max_concurrency": 1})
	return text_summaries

def embedSummaries(data):
	modelPath = "sentence-transformers/all-MiniLM-l6-v2"
	model_kwargs = {'device':'cpu'}
	encode_kwargs = {'normalize_embeddings': False}
	embeddings = HuggingFaceEmbeddings(
		model_name=modelPath,     # Provide the pre-trained model's path
    	model_kwargs=model_kwargs, # Pass the model configuration options
    	encode_kwargs=encode_kwargs # Pass the encoding options
	)


	query_result = FAISS.from_texts(data, embeddings)
	

	return query_result




if __name__=="__main__":
	fd = load_pdf(pdf_folder_path,pdf_file_name)
	st = splitText(fd)
	summ = summarizeData(st,lm)
	e = embedSummaries(summ)

	
	print(f'Summary: {summ}')


#

#def generateSummary():
