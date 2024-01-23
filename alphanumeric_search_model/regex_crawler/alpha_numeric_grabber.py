import requests
import json
import spacy
import re

from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.training.example import Example

query = {
    "sort": [
        {
            "_score" :{ "order" : "desc"}
        }
    ],
    "size" : 100,
    "query" : {
        "bool" :{
            "must" : [
                # {
                #     "match": {
                #         "title_en": {
                #             "query": "DD 214*"
                #         }
                #     }
                # },
            ],
            "filter": [
                # {
                #     "regexp": {
                #         "SOME_IMPORTANT_FIELD": {
                #             "value": "SOME_REGEX_PATTERN",
                #             "case_insensitive": True
                #         }
                #     }
                # },
                {
                    "exists": {
                        "field": "content_en"
                    }
                },
                {
                    "bool": {
                        "should" : [
                            {
                                "term": {
                                    "domain_name": "static.e-publishing.af.mil"
                                }
                            },
                            {
                                "term": {
                                    "domain_name": "www.e-publishing.af.mil"
                                }
                            },
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
                            # }
                        ]
                    }
                }
            ]
        }
    }
}

indices = {
    "production-i14y-documents-searchgov-v6-reindex_keyword" : [
        "title_en",
        # "title_en.raw.keyword",
        "content_en",
        # "content_en.raw.keyword"
    ],
    # "human_logstash-*": [
    #     "params.query.raw"
    # ]
}

es_urls = [
    # "http://localhost:9200"
    "http://es717x1:9200",
    "http://es717x2:9200",
    "http://es717x3:9200",
    "http://es717x4:9200",
]

# Although Python will do case insensitive searching for regex patterns, ES 7.17 doesn't appear to 
# do searching with case insensitivity enabled.
regex_expressions = [
    # "[0-9]+[a-z]+",
    # # "[0-9]+[A-Z]+",

    # "[a-z]+[0-9]+",
    # # "[A-Z]+[0-9]+",

    "[a-z]+[0-9]+-[a-z]+[0-9]*",
    # "[A-Z]+[0-9]+-[a-z]+[0-9]*",
    # "[a-z]+[0-9]+-[A-Z]+[0-9]*",
    # "[A-Z]+[0-9]+-[A-Z]+[0-9]*",

    "[a-z]+[0-9]*-[a-z]+[0-9]+",
    # "[A-Z]+[0-9]*-[a-z]+[0-9]+",
    # "[a-z]+[0-9]*-[A-Z]+[0-9]+",
    # "[A-Z]+[0-9]*-[A-Z]+[0-9]+",

    "[a-z]+[0-9]+-[0-9]+[a-z]*",
    # "[a-z]+[0-9]+-[0-9]+[A-Z]*",
    # "[A-Z]+[0-9]+-[0-9]+[a-z]*",
    # "[A-Z]+[0-9]+-[0-9]+[A-Z]*",
    
    "[a-z]+[0-9]*-[0-9]+[a-z]+",
    # "[a-z]+[0-9]*-[0-9]+[A-Z]+",
    # "[A-Z]+[0-9]*-[0-9]+[a-z]+",
    # "[A-Z]+[0-9]*-[0-9]+[A-Z]+",

    "[0-9]+[a-z]+-[a-z]+[0-9]*",
    # "[0-9]+[A-Z]+-[a-z]+[0-9]*",
    # "[0-9]+[a-z]+-[A-Z]+[0-9]*",
    # "[0-9]+[A-Z]+-[A-Z]+[0-9]*",

    "[0-9]+[a-z]*-[a-z]+[0-9]+",
    # "[0-9]+[A-Z]*-[a-z]+[0-9]+",
    # "[0-9]+[a-z]*-[A-Z]+[0-9]+",
    # "[0-9]+[A-Z]*-[A-Z]+[0-9]+",

    "[0-9]+[a-z]*-[0-9]+[a-z]+",
    # "[0-9]+[A-Z]*-[0-9]+[a-z]+",
    # "[0-9]+[a-z]*-[0-9]+[A-Z]+",
    # "[0-9]+[A-Z]*-[0-9]+[A-Z]+",

    "[0-9]+[a-z]+-[0-9]+[a-z]*",
    # "[0-9]+[A-Z]+-[0-9]+[a-z]*",
    # "[0-9]+[a-z]+-[0-9]+[A-Z]*",
    # "[0-9]+[A-Z]+-[0-9]+[A-Z]*",

    # Sections, leaving this disabled for now
    # # "([a-z]+[0-9]*§[a-z]+[0-9]*)",
    # # "([a-z]+[0-9]*§[0-9]+[a-z]*)",
    # # "([0-9]+[a-z]*§[a-z]+[0-9]*)",
    # # "([0-9]+[a-z]*§[0-9]+[a-z]*)",
    # # "([a-z]+[0-9]*.[a-z]+[0-9]*)",

    "[a-z]+[0-9]*\\.[a-z]+[0-9]+",
    # "[A-Z]+[0-9]*\\\.[a-z]+[0-9]+",
    # "[a-z]+[0-9]*\\\.[A-Z]+[0-9]+",
    # "[A-Z]+[0-9]*\\\.[A-Z]+[0-9]+",

    "[a-z]+[0-9]+\\.[a-z]+[0-9]*",
    # "[A-Z]+[0-9]+\\\.[a-z]+[0-9]*",
    # "[a-z]+[0-9]+\\\.[A-Z]+[0-9]*",
    # "[A-Z]+[0-9]+\\\.[A-Z]+[0-9]*",

    "[a-z]+[0-9]+\\.[a-z]+[0-9]+",
    # "[A-Z]+[0-9]+\\\.[a-z]+[0-9]+",
    # "[a-z]+[0-9]+\\\.[A-Z]+[0-9]+",
    # "[A-Z]+[0-9]+\\\.[A-Z]+[0-9]+",

    "[a-z]+[0-9]*\\.[0-9]+[a-z]*",
    # "[a-z]+[0-9]*\\\.[0-9]+[A-Z]*",
    # "[A-Z]+[0-9]*\\\.[0-9]+[a-z]*",
    # "[A-Z]+[0-9]*\\\.[0-9]+[A-Z]*",

    "[0-9]+[a-z]*\\.[a-z]+[0-9]*",
    # "[0-9]+[A-Z]*\\\.[a-z]+[0-9]*",
    # "[0-9]+[a-z]*\\\.[A-Z]+[0-9]*",
    # "[0-9]+[A-Z]*\\\.[A-Z]+[0-9]*",

    "[0-9]+[a-z]*\\.[0-9]+[a-z]+",
    # "[0-9]+[A-Z]*\\\.[0-9]+[a-z]+",
    # "[0-9]+[a-z]*\\\.[0-9]+[A-Z]+",
    # "[0-9]+[A-Z]*\\\.[0-9]+[A-Z]+",
    
    "[0-9]+[a-z]+\\.[0-9]+[a-z]*",
    # "[0-9]+[A-Z]+\\\.[0-9]+[a-z]*",
    # "[0-9]+[a-z]+\\\.[0-9]+[A-Z]*",
    # "[0-9]+[A-Z]+\\\.[0-9]+[A-Z]*",
        
    "[a-z]+[0-9]* [a-z]+[0-9]+",
    # "[A-Z]+[0-9]* [a-z]+[0-9]+",
    # "[a-z]+[0-9]* [A-Z]+[0-9]+",
    # "[A-Z]+[0-9]* [A-Z]+[0-9]+",

    "[a-z]+[0-9]+ [a-z]+[0-9]*",
    # "[A-Z]+[0-9]+ [a-z]+[0-9]*",
    # "[a-z]+[0-9]+ [A-Z]+[0-9]*",
    # "[A-Z]+[0-9]+ [A-Z]+[0-9]*",

    "[a-z]+[0-9]* [0-9]+[a-z]*",
    # "[A-Z]+[0-9]* [0-9]+[a-z]*",
    # "[a-z]+[0-9]* [0-9]+[A-Z]*",
    # "[A-Z]+[0-9]* [0-9]+[A-Z]*",

    "[0-9]+[a-z]* [a-z]+[0-9]*",
    # "[0-9]+[A-Z]* [a-z]+[0-9]*",
    # "[0-9]+[a-z]* [A-Z]+[0-9]*",
    # "[0-9]+[A-Z]* [A-Z]+[0-9]*",

    "[0-9]+[a-z]+ [0-9]+[a-z]*",
    # "[0-9]+[A-Z]+ [0-9]+[a-z]*",
    # "[0-9]+[a-z]+ [0-9]+[A-Z]*",
    # "[0-9]+[A-Z]+ [0-9]+[A-Z]*",

    "[0-9]+[a-z]* [0-9]+[a-z]+",
    # "[0-9]+[a-z]* [0-9]+[a-z]+",
    # "[0-9]+[a-z]* [0-9]+[a-z]+",
    # "[0-9]+[a-z]* [0-9]+[a-z]+",
]

def query_elasticsearch(es_url, search_endpoint, body = ""):
    r = requests.get(
        es_url + search_endpoint, 
        headers = {"Content-Type": "application/json"},
        data=body
        )
    return r

def create_scroll_elasticsearch(url, index, body, scroll_duration):
    return query_elasticsearch(
        url,
        "/" + index + "/_search?scroll=" + str(scroll_duration) + "m",
        body
    )

def clear_scroll_context(url, scroll_id):
    return requests.delete(
        url + "/_search/scroll/" + str(scroll_id)
    )

def push_to_elasticsearch(url, index, documents):
    # Use Partial document update to push to ElasticSearch
    es_payload = []
    for document in documents:
        es_payload.append(json.dumps({"index" : {"_index": index}}))
        es_payload.append(json.dumps({"doc" : document}))
    tmp = requests.post(
        url + "/_bulk",
        headers = {"Content-Type": "application/json"},
        data="\n".join(es_payload) + "\n"
    )
    return tmp

def verify_alphanumeric_values(values):
    # print(values)
    new_values = []
    for alphanumeric in values:
        punc_free = re.sub("[-\s\.]", "", alphanumeric)
        # print(alphanumeric, "\t", punc_free, "\t", re.sub("\d", "", punc_free).isalpha(), "\t", re.sub("[a-zA-Z]", "", punc_free).isnumeric())
        if re.sub("\d", "", punc_free).isalpha() and re.sub("[a-zA-Z]", "", punc_free).isnumeric():
            new_values.append(alphanumeric)
    return new_values

def create_i14y_doc(doc, regex, field):
    # print(regex, "\t", doc["_source"][field])
    # print(re.findall(regex.replace("\\\\", "\\"), doc["_source"][field]))
    # verify_alphanumeric_values(re.findall(regex.replace("\\\\", "\\"), doc["_source"][field]))
    return {
        "domain_name" : doc["_source"]["domain_name"],
        "regex_patterns" : verify_alphanumeric_values(re.findall(regex.replace("\\\\", "\\"), doc["_source"][field], re.IGNORECASE))
    }
    # return

def crawl_es_index(es_url, index):
    # modified_query = json.dumps(query).replace("SOME_REGEX_PATTERN", regex_pattern).replace("SOME_IMPORTANT_FIELD", field)
    results = create_scroll_elasticsearch(es_url[0], index, json.dumps(query), 60)
    json_result = results.json()
    # docs_processed = 0
    es_node = 0

    # print(json_result)

    if(results.status_code == 400):
        print(json_result)
        return

    print("Num Docs: ", len(json_result["hits"]["hits"]))

    scroll_id = json_result["_scroll_id"]
    some_int = 0
    # while True:
    while some_int < 2:
        # print(doc_count, "\t", docs_processed, "\t", (doc_count - docs_processed))
        if len(json_result["hits"]["hits"]) == 0:
            # clear_scroll_context(es_url[es_node], scroll_id)
            break
        
        # if docs_processed > 20:
        #     break
        
        temp_doc_list = []

        # print(temp_doc_list)

        for document in json_result["hits"]["hits"]:
            for field in indices[index]:
                # scan_field = field.replace(".raw", "").replace(".keyword", "")
                # regex_pattern = regex_expressions[0]
                for regex_pattern in regex_expressions:
                    print(" ****************** ", field, ": ", regex_pattern, " ****************** ")
                    temp_doc_list.append(create_i14y_doc(document, regex_pattern, field))
            # docs_processed = docs_processed + 1
        
        # print(temp_doc_list)

        response = push_to_elasticsearch(es_url[es_node], index + "_regex_py", temp_doc_list)
        if(response.status_code == 400):
            print(response.json())
            # return
            
        results = query_elasticsearch(es_url[es_node], "/_search/scroll", json.dumps({
            "scroll" : "10m",
            "scroll_id": scroll_id
        }))
        json_result = results.json()
        es_node = (es_node + 1) % len(es_urls)
        some_int = some_int + 1
    # return
    clear_scroll_context(es_url[es_node], scroll_id)


for index in list(indices.keys()):
    # for field in indices[index]:
        # for regexp in regex_expressions:
    # print(" ****************** ", field, ": ", regexp, " ****************** ")
    # count_query = query.copy()
    # del count_query["sort"]
    # del count_query["size"]
    # modified_query = json.dumps(count_query).replace("SOME_REGEX_PATTERN", regexp).replace("SOME_IMPORTANT_FIELD", field)
    # result = query_elasticsearch(es_urls[0], "/" + index + "/_count", modified_query)
    crawl_es_index(es_urls, index)
