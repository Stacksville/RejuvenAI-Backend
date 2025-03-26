from vectordb import get_vectordb

def main(): 
    vectordb = get_vectordb()

    query = "why is attention important?"
    docs = vectordb.similarity_search(query)

    print(docs)

if __name__ == '__main__': 
    main()
    

