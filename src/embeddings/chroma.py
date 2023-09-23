import chromadb
from chromadb.utils import embedding_functions
from .. import chromadb_path, OPENAI_API_KEY, openai_embedding_model, current_directory
import pandas as pd
import gdown

# if technique embeddings not present download from notabug
def download_csv_from_gdrive(type_='cve'):
    if type_=='cve':
        url = 'https://drive.google.com/file/d/12J75g-Xs7WBv-rvL3enW93Z4UxDlW446/view?usp=sharing'
        output = current_directory+'/src/embeddings/chromadb/cve_embeddings_ada.csv'
    elif type_=='technique':
        url = 'https://drive.google.com/file/d/1bwCoyUQZlKisHg4JmmC0ZIAfdW3Vc_SL/view?usp=sharing'
        output = current_directory+'/src/embeddings/chromadb/technique_embeddings_ada.csv'
    gdown.download(url, output, quiet=False, fuzzy=True)
    df = pd.read_csv(output)
    print(df)
    print(f'Loaded {type_} embeddings from drive with shape {df.shape}')
    return df

client = chromadb.PersistentClient(path=chromadb_path)

embedder = embedding_functions.OpenAIEmbeddingFunction(
     api_key = OPENAI_API_KEY,
     model_name = openai_embedding_model
)

chroma_openai_cwe_collection = client.create_collection(
        name = "chroma_openai_cwe",
        embedding_function=embedder,
        get_or_create = True
    )

if chroma_openai_cwe_collection.count() == 0:
    print("Loading cve embeddings from drive")
    cve_df = download_csv_from_gdrive(type_='cve')
    cve_df['embeddings'] = cve_df.embeddings.apply(eval).apply(list)
    cve_df['Technique'] = cve_df.Technique.apply(eval).apply(list)
    cve_df['Technique'] = cve_df.Technique.apply(lambda x: ", ".join(x))
    ids = [str(i) for i in range(len(cve_df))]
    documents = cve_df["description"].tolist()
    embeddings = cve_df["embeddings"].tolist()
    metadatas = []
    for idx, row in cve_df.iterrows():
        metadatas.append(
            {
                "cve":row["CVE"],
                "technique":row["Technique"],
                "cve_description_token_len":int(row["token_len"])
            }
        )
    print("adding cve embeddings to chroma collection")
    chroma_openai_cwe_collection.add(
        ids = ids,
        documents = documents,
        embeddings = embeddings,
        metadatas = metadatas
    )
    del cve_df
    print("Finished adding cve embeddings to chroma collection")
else:
    print("cve embeddings already in chroma collection")

chroma_openai_attack_collection = client.create_collection(
        name = "chroma_openai_attack",
        embedding_function=embedder,
        get_or_create = True
    )

if chroma_openai_attack_collection.count() == 0:
    print("Loading attack embeddings from drive")
    attack_df = download_csv_from_gdrive(type_='technique')
    attack_df['embeddings'] = attack_df.embeddings.apply(eval).apply(list)
    ids = [str(i) for i in range(len(attack_df))]
    documents = attack_df["description"].tolist()
    embeddings = attack_df["embeddings"].tolist()
    metadatas = []
    for idx, row in attack_df.iterrows():
        metadatas.append(
            {
                "technique":row["Technique"],
                "technique_description_token_len": int(row["token_len"])
            }
        )
    print("adding attack embeddings to chroma collection")
    chroma_openai_attack_collection.add(
        ids = ids,
        documents = documents,
        embeddings = embeddings,
        metadatas = metadatas
    )
    del attack_df
    print("Finished adding attack embeddings to chroma collection")
else:
    print("attack embeddings already in chroma collection")    

severity_file_path = current_directory+'/src/nl_to_sql/severity.txt'
with open(severity_file_path,'r') as f:
    severities = [s.strip() for s in f.readlines()]

chroma_openai_severity_collection = client.create_collection(
        name = "chroma_openai_severity",
        embedding_function=embedder,
        get_or_create = True
    )

if chroma_openai_severity_collection.count() == 0:
    ids = [str(i) for i in range(len(severities))]
    documents = severities
    print("adding severity embeddings to chroma collection")
    chroma_openai_attack_collection.add(
        ids = ids,
        documents = documents
    )
    print("Finished adding severity embeddings to chroma collection")
else:
    print("severity embeddings already in chroma collection")   

# CLIENT methods
# # list all collections
# client.list_collections()

# # make a new collection
# collection = client.create_collection("testname")

# # get an existing collection
# collection = client.get_collection("testname")

# # get a collection or create if it doesn't exist already
# collection = client.get_or_create_collection("testname")

# # delete a collection
# client.delete_collection("testname")

# COLLECTION methods
# # change the name or metadata on a collection
# collection.modify(name="testname2")

# # get the number of items in a collection
# collection.count()

# # add new items to a collection
# # either one at a time
# collection.add(
#     embeddings=[1.5, 2.9, 3.4],
#     metadatas={"uri": "img9.png", "style": "style1"},
#     documents="doc1000101",
#     ids="uri9",
# )
# # or many, up to 100k+!
# collection.add(
#     embeddings=[[1.5, 2.9, 3.4], [9.8, 2.3, 2.9]],
#     metadatas=[{"style": "style1"}, {"style": "style2"}],
#     ids=["uri9", "uri10"],
# )
# collection.add(
#     documents=["doc1000101", "doc288822"],
#     metadatas=[{"style": "style1"}, {"style": "style2"}],
#     ids=["uri9", "uri10"],
# )

# # update items in a collection
# collection.update()

# # upsert items. new items will be added, existing items will be updated.
# collection.upsert(
#     ids=["id1", "id2", "id3", ...],
#     embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2], ...],
#     metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}, ...],
#     documents=["doc1", "doc2", "doc3", ...],
# )

# # get items from a collection
# collection.get()

# # convenience, get first 5 items from a collection
# collection.peek()

# # do nearest neighbor search to find similar embeddings or documents, supports filtering
# collection.query(
#     query_embeddings=[[1.1, 2.3, 3.2], [5.1, 4.3, 2.2]],
#     n_results=2,
#     where={"style": "style2"}
# )

# # delete items
# collection.delete()