from gqlalchemy import Memgraph, Node, Relationship, Field
from typing import Optional
from csv import DictReader
from os.path import join

db = Memgraph(host='127.0.0.1', port=7687)
db.drop_database()


class Author(Node):
    uuid: str = Field(unique=True, index=True, db=db)
    orcid: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]


class Output(Node):
    doi: str = Field(unique=True, index=True, db=db)


class Article(Output):
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
                                                last_name=author['First Name'],
                                                first_name=author['Last Name'],
                                                orcid=author['Orcid']).save(db)

output_objects = {}
with open(join('data', 'papers.csv')) as papers_csv:
    reader = DictReader(papers_csv)
    for output in reader:
        print(output)
        output_objects[output['DOI']] = Article(doi=output['DOI'],
                                                title=output['title'],
                                                abstract=output['Abstract']).save(db)

with open(join('data', 'relations.csv')) as relations_csv:
    reader = DictReader(relations_csv)
    for rel in reader:
        uuid = rel['uuid']
        doi = rel['doi']

        loaded_author = Author(uuid=uuid).load(db=db)
        loaded_output = Article(doi=doi).load(db=db)

        author_of(_start_node_id=loaded_author._id, _end_node_id=loaded_output._id).save(db)
