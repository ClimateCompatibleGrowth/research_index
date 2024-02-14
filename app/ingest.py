from gqlalchemy import Memgraph, Node, Relationship, Field
from typing import Optional
from csv import DictReader
from os.path import join
from os import environ

MG_HOST = environ.get('MG_HOST', '127.0.0.1')
MG_PORT = int(environ.get('MG_PORT', 7687))

db = Memgraph(host=MG_HOST, port=MG_PORT)
db.drop_database()


class Author(Node):
    uuid: str = Field(unique=True, index=True, db=db)
    orcid: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]


class Output(Node):
    uuid: str = Field(unique=True, index=True, db=db)


class Article(Output):
    doi: Optional[str]
    title: Optional[str]
    abstract: Optional[str]


class author_of(Relationship):
    pass


author_objects = {}
with open(join('data', 'authors.csv')) as authors_csv:
    reader = DictReader(authors_csv)
    for author in reader:
        print(author)
        author_objects[author['uuid']] = Author(uuid=author['uuid'],
                                                first_name=author['First Name'],
                                                last_name=author['Last Name'],
                                                orcid=author['Orcid']).save(db)

output_objects = {}
with open(join('data', 'papers.csv')) as papers_csv:
    reader = DictReader(papers_csv)
    for output in reader:
        print(output)
        output_objects[output['paper_uuid']] = Article(uuid=output['paper_uuid'],
                                                       doi=output['DOI'],
                                                       title=output['title'],
                                                       abstract=output['Abstract']).save(db)

with open(join('data', 'relations.csv')) as relations_csv:
    reader = DictReader(relations_csv)
    for rel in reader:
        author_uuid = rel['uuid']
        paper_uuid = rel['paper_uuid']

        loaded_author = Author(uuid=author_uuid).load(db=db)
        loaded_output = Article(uuid=paper_uuid).load(db=db)

        author_of(_start_node_id=loaded_author._id, _end_node_id=loaded_output._id).save(db)
