from langchain.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter #Tách văn bản kí tự đệ quy
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F



#Các hàm tiện ích 

def load_pdf_file(data):
    loader = DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)
    documents=loader.load()

    return documents




#Phân thành các đoạn văn bản -> thành các chunck

def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500 , chunk_overlap=20) #dài 500 và và lặp lại từ 20 từ -> tiếp theo
    text_chucks=text_splitter.split_documents(extracted_data) #split_documents là của RecursiveCharacterTextSplitter
    return text_chucks





# Class để xử lý embedding
class HuggingFaceEmbeddings:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        # Load tokenizer và model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def embed_query(self, sentence: str) -> list[float]:
        encoded_input = self.tokenizer(sentence, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embedding = self.mean_pooling(model_output, encoded_input['attention_mask'])
        # Chuẩn hóa vector
        sentence_embedding = F.normalize(sentence_embedding, p=2, dim=1)
        # Chuyển sang list để Pinecone serialize được
        return sentence_embedding[0].cpu().numpy().tolist()


    def embed_documents(self, sentences: list):
        """Embedding cho danh sách câu"""
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings.cpu().numpy()
    
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings()
    return embeddings