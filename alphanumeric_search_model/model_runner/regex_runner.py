# Load Spacy Model
# Load Levenshtein Dictionary
# Query ElasticSearch for Documents
# Consider partial document updates...

import argparse
# import spacy
import json
import sys
import datetime
import signal
import re
import memory_profiler
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from guppy import hpy
from memory_profiler import profile

query = {
    "query" : {
        "bool": {
            "must": [
                {
                    "range" : {
                        "updated_at": {
                            "gte": "SOME_VALUE",
                            "lte": "now"
                        }
                    }
                # },
                # {
                #     "query_string": {
                #         "query": "18th",
                #         "default_field": "content_en"
                #     }
                # },
                # {
                #     "query_string": {
                #         "query": "www.e-publishing.af.mil",
                #         "default_field": "domain_name"
                #     }
                }
            ],
            "filter": [
                {
                    "exists": {
                        "field": "content_en"
                    }
                },
                {
                    "bool": {
                        "should" : [
                            # {
                            #     "term": {
                            #         "domain_name": "static.e-publishing.af.mil"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.e-publishing.af.mil"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.goarmy.com"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.gsa.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.uscis.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.va.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "apps.dtic.mil"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.nrc.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.fs.usda.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.justice.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.sec.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.army.mil"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "founders.archives.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.cdc.gov"
                            #     }
                            # },
                            # {
                            #     "term": {
                            #         "domain_name": "www.osha.gov"
                            #     }
                            # },
                        ]
                    }
                }
            ],
            "should": [

            ],
            "must_not": [

            ]
        }
        # {},
        # {"query_string": {
        #     "query": "community",
        #     "default_field": "content_en"
        # }}
        # #,
        # # "exists": {
        # #     "field": "SOME_FIELD"
        # # }
    },
    "size" : 100
}

regex_patterns = [
    "[0-9]+[a-z]+",
    "[a-z]+[0-9]+",

    "[a-z]+[0-9]+-[a-z]+[0-9]*",
    "[a-z]+[0-9]*-[a-z]+[0-9]+",
    "[a-z]+[0-9]+-[0-9]+[a-z]*",
    "[a-z]+[0-9]*-[0-9]+[a-z]+",
    "[0-9]+[a-z]+-[a-z]+[0-9]*",
    "[0-9]+[a-z]*-[a-z]+[0-9]+",
    "[0-9]+[a-z]*-[0-9]+[a-z]+",
    "[0-9]+[a-z]+-[0-9]+[a-z]*",

    # Sections, leaving this disabled for now
    # # "([a-z]+[0-9]*§[a-z]+[0-9]*)",
    # # "([a-z]+[0-9]*§[0-9]+[a-z]*)",
    # # "([0-9]+[a-z]*§[a-z]+[0-9]*)",
    # # "([0-9]+[a-z]*§[0-9]+[a-z]*)",
    # # "([a-z]+[0-9]*.[a-z]+[0-9]*)",

    # Add Forward Slashes AFSOC/A3V

    "[a-z]+[0-9]*\\.[a-z]+[0-9]+",
    "[a-z]+[0-9]+\\.[a-z]+[0-9]*",
    "[a-z]+[0-9]+\\.[a-z]+[0-9]+",
    "[a-z]+[0-9]*\\.[0-9]+[a-z]*",
    "[0-9]+[a-z]*\\.[a-z]+[0-9]*",
    "[0-9]+[a-z]*\\.[0-9]+[a-z]+",
    "[0-9]+[a-z]+\\.[0-9]+[a-z]*",

    "[a-z]+[0-9]* [a-z]+[0-9]+",
    "[a-z]+[0-9]+ [a-z]+[0-9]*",
    "[a-z]+[0-9]* [0-9]+[a-z]*",
    "[0-9]+[a-z]* [a-z]+[0-9]*",
    "[0-9]+[a-z]+ [0-9]+[a-z]*",
    "[0-9]+[a-z]* [0-9]+[a-z]+",
]

parser = argparse.ArgumentParser(
    prog = "Some Insightful Name",
    description = "What this script does"
)

h = hpy()

# parser.add_argument("-s", "--start_date", required=True, help="Date and time to from which to start processing documents MM-DD-YYYY HH:mm")
# parser.add_argument("-e", "--es_url", required=True, help="The URL of ElasticSearch, should also contain the port")
# parser.add_argument("-i", "--index", required=True, help="The Index to Crawl inside of ElasticSearch")
# Username
# Password
# Consider Ability to load different spacy models
# Consider ability to load different Levenshtein dictionaries


def query_elasticsearch(es_client, scroll_id, scroll_duration = "10m"):
    # Make Request to ElasticSearch
    # print(str(datetime.datetime.now()),"\t",request)
    return es_client.scroll(scroll_id = scroll_id, scroll=scroll_duration)

def create_scroll_elasticsearch(es_client, index, request, scroll_duration = 10):
    # Make a Scrolling request to ElasticSearch
    return es_client.search(
        index = index,
        body = request,
        scroll = str(scroll_duration) + "m"
    )

def push_to_elasticsearch(es_client, index, documents):
    # Use Partial document update to push to ElasticSearch
    es_payload = []
    for document in documents:
        es_payload.append({"update" : {"_index": index, "_id": document["id"]}})
        es_payload.append({"doc" : {"alphanumeric_values": document["alphanumeric_vals"]}})
    # es_client.bulk(body=es_payload)
    parallel_bulk(client=es_client, actions = es_payload, max_chunk_bytes=50000000)

def load_levenshtein_dictionary(file_name):
    levenshtein_dictionary = {}
    dict_file = open(file_name, "r")
    for line in dict_file:
        split_line = line.strip().split(",")
        levenshtein_dictionary[split_line[0]] = split_line[1:]
    dict_file.close()
    return levenshtein_dictionary

def create_changed_punctuation_array(word):
    punctuation_regex = "[-\s\.§]"
    punctuation_substitutions = ["-", " ", ".", "§"]
    word_array = [word, re.sub(punctuation_regex, "", word)]
    for letter in punctuation_substitutions:
        # print(letter)
        # print(word_array)
        word_array.append(re.sub(punctuation_regex, letter, word))
    
    return list(set(word_array))

def verify_alphanumeric_values(values):
    # print(values)
    new_values = []
    for alphanumeric in values:
        punc_free = re.sub("[-\s\.]", "", alphanumeric)
        # print(alphanumeric, "\t", punc_free, "\t", re.sub("\d", "", punc_free).isalpha(), "\t", re.sub("[a-zA-Z]", "", punc_free).isnumeric())
        if re.sub("\d", "", punc_free).isalpha() and re.sub("[a-zA-Z]", "", punc_free).isnumeric():
            new_values.append(alphanumeric)
    return new_values

def process_alphanumeric_document(document):
    alpha_numerics = []
    for regexp in regex_patterns:
        temp_ans = re.findall(regexp.replace("\\\\", "\\"), document, re.IGNORECASE)
        temp_ans = verify_alphanumeric_values(list(set(temp_ans)))
        for alpha_numeric in temp_ans:
            alpha_numerics.append(create_changed_punctuation_array(alpha_numeric))
            # if alpha_numeric in levenshtein_dictionary:
            #     alpha_numerics.append(levenshtein_dictionary[alpha_numeric])
    return alpha_numerics

def collect_memory_stats():
    file.write(str(datetime.datetime.now()))
    file.write(str("\n"))
    print(h.heap())
    file.write(str(h.heap()))
    file.write(str("\n"))

# @profile
def crawl_es_index(es_client, index, start_date):
    # Do the actual crawling
    # Call scroll
    num_docs_more_than_3m = 0
    modified_query = json.dumps(query).replace("SOME_VALUE", start_date).replace("SOME_FIELD", "updated_at")
    json_result = create_scroll_elasticsearch(es_client, index, modified_query, 60)
    # json_result = results.json()
    num_runs = 0
    # print(json_result)
    scroll_id = json_result["_scroll_id"]
    try:
        while True:
            # Check that there are documents to process
            if len(json_result["hits"]["hits"]) == 0:
                print("Number of documents more than 3MB: ", num_docs_more_than_3m)
                break

            if num_runs == 100:
                num_runs = 0
                # collect_memory_stats()
                print(str(datetime.datetime.now()), " Processed 10K Documents")
                es_client.refresh(index = index)
            
            # Process documents
            modified_documents = []
            for document in json_result["hits"]["hits"]:
                # print(document)
                # print(document["_id"])
                if "content_en" in document["_source"]:
                    try:
                        doc = {
                                "id": document["_id"],
                                "alphanumeric_vals": process_alphanumeric_document(document["_source"]["content_en"])
                            }
                        modified_documents.append(doc)
                        doc = None
                        # print(len(modified_documents[-1]["alphanumeric_vals"]))
                    except ValueError as why:
                        num_docs_more_than_3m = num_docs_more_than_3m + 1
            
            # Write Documents to ES
            # print(modified_documents)
            # sys.exit(0)
            if len(modified_documents) > 0:
                push_to_elasticsearch(es_client, index, modified_documents)
            modified_documents = None
            # Query ElasticSearch
            json_result = query_elasticsearch(es_client, scroll_id)
            num_runs = num_runs + 1
    except KeyboardInterrupt:
        print("Exiting")
    file.close()

# Setup Process
args = parser.parse_args()
# start_date = args.start_date
# es_url = args.es_url
# index = args.index

# alphanumeric_spacy = spacy.load("../spacy_model_training/alpha_numeric_ner_model/")
# levenshtein_dictionary = load_levenshtein_dictionary("../levenshtein_final.csv")
# alphanumeric_spacy = spacy.load("/mnt/trainingdata/ksummers/alpha_numeric_ner_model/")
# alphanumeric_spacy.max_length = 1500000
levenshtein_dictionary = load_levenshtein_dictionary("/mnt/trainingdata/ksummers/levenshtein_final.csv")

# print(levenshtein_dictionary["18th"])
# sys.exit(0)

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
str_current_datetime = str(current_datetime)
file_name = "/mnt/trainingdata/ksummers/heap_usage_" + str_current_datetime + ".txt"
# file_name = "heap_usage_" + str_current_datetime + ".txt"
file = open(file_name, 'w')


# es_url = ["http://localhost:9200/"]
es_url = ["http://es717x1:9200/", "http://es717x2:9200/", "http://es717x3:9200/", "http://es717x4:9200/"]
index = "production-i14y-documents-searchgov-v6"
start_date = "2023-01-01"

elasticsearch_client = Elasticsearch(es_url, timeout=60, retry_on_timeout = True)

# print(elasticsearch_client.search(index=index))

crawl_es_index(elasticsearch_client, index, start_date)