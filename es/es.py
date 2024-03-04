from elasticsearch import Elasticsearch

from models.blog import Post
from forms.forms import SearchForm
from flask import request, jsonify
from elasticsearch_dsl import Index

es = Elasticsearch(
    [{"host": "localhost", "port": 9200, "scheme": "http"}],
    http_auth=("elastic", "elastic")
)
index_name = 'posts'


def sync_data_to_es():
    # 连接到 SQLite 数据库
    posts = Post.query.all()
    # 定义索引映射
    index_mappings = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "ik_max_word",  # 使用standard分析器
                "search_analyzer": "ik_max_word"  # 搜索时也使用standard分析器
            },
            "content": {
                "type": "text",
                "analyzer": "ik_max_word",  # 使用standard分析器
                "search_analyzer": "ik_max_word"  # 搜索时也使用standard分析器
            },
            "tags": {
                "type": "text",
                "analyzer": "ik_max_word",  # 使用standard分析器
                "search_analyzer": "ik_max_word"  # 搜索时也使用standard分析器
            },
            "date_posted": {
                "type": "date"

            },
            "updated_at": {
                "type": "date"
            }
        }
    }
    # 检查索引是否存在，如果不存在则创建索引并定义映射
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, mappings=index_mappings)
    # 将数据同步到 Elasticsearch
    for row in posts:
        post_tags = [tag.name for tag in row.tags]
        doc = {
            'title': row.title,
            'content': row.content,
            'date_updated': row.date_posted,
            'updated_at': row.updated_at,
            'tags': post_tags
        }
        es.index(index=index_name, body=doc)


def search():
    query = request.args.get('query')
    if query:
        results = es.search(index=index_name, body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "content", "tags"]
                }
            },
            "highlight": {
                "fields": {
                    "title": {
                        "fragment_size": 100,
                        "number_of_fragments": 1
                    },
                    "content": {
                        "fragment_size": 300,
                        "number_of_fragments": 100
                    },
                    "tags": {
                        "fragment_size": 100,
                        "number_of_fragments": 50
                    }
                }
            }
        })
        return jsonify(results['hits']['hits'])
