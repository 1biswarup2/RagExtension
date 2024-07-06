from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

def html_splitter(urls):
    loader = AsyncHtmlLoader(urls)
    html2text = Html2TextTransformer()

    docs = loader.load()
    docs_transformed = html2text.transform_documents(docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, 
                                                    chunk_overlap = 500, 
                                                    length_function=len,
                                                    is_separator_regex=False,
                                                    separators=[
                                                                "#","##","###","####","\n\n", "\n",".",",",
                                                                "\u200B",  # Zero-width space
                                                                "\uff0c",  # Fullwidth comma
                                                                "\u3001",  # Ideographic comma
                                                                "\uff0e",  # Fullwidth full stop
                                                                "\u3002",  # Ideographic full stop
                                                                ])
    splits = text_splitter.split_documents(docs_transformed)
    # print(splits)
    return splits