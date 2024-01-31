import base64
import json
import logging
import sys
import os

from llama_index import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index import ServiceContext
from llama_index import set_global_service_context
from llama_index import download_loader
from IPython.display import Markdown, display

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

with open("sources.urls") as f:
     urls = json.load(f)

docs_read = 0
ReadabilityWebPageReader = download_loader("ReadabilityWebPageReader")
loader = ReadabilityWebPageReader()

# TODO: Write the downloaded files to local directory "data"
for u in urls:
    try:
        if u.get("url", None):
            base64str = base64.urlsafe_b64encode(bytes(u["url"], 'utf-8'))
            base64str = base64str.decode('utf-8')
            pathname = os.path.join("data", base64str)

            #documents = SimpleWebPageReader(html_to_text=True).load_data([u.get("url")])
            documents = loader.load_data(url=u["url"])
            with open(pathname, "w") as f:
                f.write(documents[0].text)
            docs_read += 1
    except Exception as ex:
        print("Error reading %s" % u.get("url"))
        print(ex)

import pdb;pdb.set_trace()
service_context = ServiceContext.from_defaults(embed_model="local")
set_global_service_context(service_context)

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
