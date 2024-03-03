from elasticsearch import Elasticsearch

from models.blog import Post

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
                          "analyzer": "ik_max_word",
                          "search_analyzer": "ik_max_word",
                          "fielddata": True},
                "content": {"type": "text",
                          "analyzer": "ik_max_word",
                          "search_analyzer": "ik_max_word",
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
    query = '语法'
    results = es.search(index=index_name, body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content"]
            }
        }
    })
    return results['hits']['hits'][0]['_source']['content']
