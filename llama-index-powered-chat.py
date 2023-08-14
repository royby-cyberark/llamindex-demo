import os
import shutil

from dotenv import load_dotenv
load_dotenv()

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage



PERSIST_DIR = "./storage"
DATA_DIR = "./data"


class GptDataIndex:

    def __init__(self):
        self.index = None
        self.persist_dir = PERSIST_DIR
        self.data_dir = DATA_DIR
        if os.path.exists(self.persist_dir):
            self._read_from_storage()
        else:
            self._build_storage()
        self.query_engine = self.index.as_query_engine()

    def query(self, query: str):
        response = self.query_engine.query(query)
        print(response)
        print()

    def _build_storage(self):
        print('Building persistence storage...')
        documents = SimpleDirectoryReader(self.data_dir).load_data()
        self.index = GPTVectorStoreIndex.from_documents(documents)
        self.index.storage_context.persist()
        print('Done.')

    def _read_from_storage(self):
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
        self.index = load_index_from_storage(storage_context)


def main(): 
    if os.path.isdir(PERSIST_DIR):
        if input("Do you want to rebuild the index? (y/enter to skip): ") == "y":
            shutil.rmtree(PERSIST_DIR)
            
    gtp_data_index = GptDataIndex()

    while user_input := input("Enter your query: (q to quit): "):
        if user_input == "q":
            break
        
        gtp_data_index.query(user_input)


if __name__ == '__main__':
    main()
