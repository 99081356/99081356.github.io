from elasticsearch import Elasticsearch

from models.blog import Post
from forms.forms import SearchForm
from flask import request,jsonify

es = Elasticsearch(
    [{"host": "localhost", "port": 9200, "scheme": "http"}],
    http_auth=("elastic", "elastic")
)
index_name = 'posts'


def sync_data_to_es():
    # 连接到 SQLite 数据库
    posts = Post.query.all()
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, mappings={
            "properties": {
                "title": {"type": "text",
                          "analyzer": "standard",
                          "search_analyzer": "whitespace",
                          "fielddata": True},
                "content": {"type": "text",
                            "analyzer": "standard",
                            "search_analyzer": "whitespace",
                            "fielddata": True},
                "date_posted": {"type": "date"},
                "update_at": {"type": "date"}
            }
        })
    # 将数据同步到 Elasticsearch
    for row in posts:
        doc = {
            'title': row.title,
            'content': row.content,
            'date_updated': row.date_posted,
            'updated_at': row.updated_at
        }
        es.index(index=index_name, body=doc)


def search():
    query = request.args.get('query')
    if query:
        results = es.search(index=index_name, body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "content"]
                }
            },
            "highlight": {
                "fields": {
                    "title": {
                        "fragment_size": 100,
                        "number_of_fragments": 1
                    },
                    "content": {
                        "fragment_size": 100,
                        "number_of_fragments": 1
                    }
                }
            }
        })
        return results['hits']['hits']
