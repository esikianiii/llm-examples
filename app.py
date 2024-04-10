from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
import gradio as gr
from langchain_community.llms import Ollama

db = Chroma(persist_directory='content/Sugar cane/db', embedding_function=HuggingFaceEmbeddings())

retriever = db.as_retriever()

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

instruction = "Given the context that has been provided. \n {context}, Answer the following question - \n{question}"

system_prompt = """You are an expert in sugar cane cultivation.
Be precise in your answers and give answers as concise as possible."""


def get_prompt(instruction, system_prompt):
    SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
    prompt_template =  B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template

template = get_prompt(instruction, system_prompt)

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

memory = ConversationBufferWindowMemory(
    memory_key="chat_history", k=5,
    return_messages=True
)

class ChatBot:
  def __init__(self, memory, prompt, retriever = retriever):
    self.memory = memory
    self.prompt = prompt
    self.retriever = retriever

  def create_chat_bot(self):
    llm = Ollama(model="llama2")
    qa = ConversationalRetrievalChain.from_llm(
      llm=llm,
      retriever=self.retriever,
      memory=self.memory,
      combine_docs_chain_kwargs={"prompt": self.prompt}
    )
    return qa
  
chatbot = ChatBot(memory = memory, prompt = prompt)

bot = chatbot.create_chat_bot()

def clear_llm_memory():
  bot.memory.clear()

def update_prompt(sys_prompt):
  if sys_prompt == "":
    sys_prompt = system_prompt
  template = get_prompt(instruction, sys_prompt)

  prompt = PromptTemplate(template=template, input_variables=["context", "question"])

  bot.combine_docs_chain.llm_chain.prompt = prompt

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(label="Chat Bot", height = 300)
    msg = gr.Textbox(label = "Question")
    clear = gr.ClearButton([msg, chatbot])
    clear_memory = gr.Button(value = "Clear LLM Memory")