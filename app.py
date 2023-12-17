from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, SDO


app = Flask(__name__)
api = Api(app)


g = Graph(bind_namespaces="rdflib")
g.parse('authors.ttl', format='turtle')




class Authors(Resource):

    resource_fields = {
        'id': fields.String,
        'givenName': fields.String,
        'familyName': fields.String,
        'gender': fields.String
    }

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        query_object = """
            SELECT ?id ?givenName ?familyName ?gender
            WHERE {
                ?id a sdo:Person ;
                    sdo:givenName ?givenName ;
                    sdo:familyName ?familyName ;
                    sdo:gender ?gender .

            }
            """
        result = g.query(query_object, initNs={'sdo': SDO})

        return [{'id': result.id,
                 'givenName': result.givenName,
                 'familyName': result.familyName,
                 'gender': result.gender} for result in result]


def abort_if_author_doesnt_exist(author_id):
    if author_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class Author(Resource):

    def get(self, id):
        query_object = """
        SELECT ?givenName ?familyName ?gender
        WHERE {
            ?id a sdo:Person ;
                sdo:givenName ?givenName ;
                sdo:familyName ?familyName ;
                sdo:gender ?gender .
            }
        """
        result = g.query(query_object,
                         initNs={'sdo': SDO},
                         initBindings={'id': URIRef(id)})

        return [{'id': result.id,
                 'givenName': result.givenName,
                 'familyName': result.familyName,
                 'gender': result.gender} for result in result]


api.add_resource(Authors, '/authors')
api.add_resource(Author, '/authors/<id>')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
