from gqlalchemy import Memgraph, match, Node
from gqlalchemy.query_builders.memgraph_query_builder import Operator


db = Memgraph(host='127.0.0.1', port=7687)


class Author:

    def get(self, id):
        """

        Notes
        -----
        MATCH (a:Author)-[r:author_of]->(p:Article)
        WHERE a.uuid = $uuid
        RETURN *;

        """
        author_query = """MATCH (a:Author) WHERE a.uuid = $uuid RETURN *;"""
        author = list(db.execute_and_fetch(author_query, parameters={'uuid': id}))[0]['a'].dict()

        collab_query = """MATCH (a:Author)-[r:author_of]->(p:Article)<-[s:author_of]-(b:Author)
                          WHERE a.uuid = $uuid
                          RETURN DISTINCT b.uuid as uuid, b.first_name as first_name, b.last_name as last_name, b.orcid as orcid"""
        colabs = list(db.execute_and_fetch(collab_query, parameters={'uuid': id}))

        author['collaborators'] = colabs

        publications_query = """MATCH (a:Author)-[r:author_of]->(p:Article) WHERE a.uuid = $uuid RETURN p.doi as doi, p.title as title;"""
        result = list(db.execute_and_fetch(publications_query, parameters={'uuid': id}))
        print(result)
        author['outputs'] = result

        return author


class AuthorModel:

    authors = {
        1:  {
                "id": 1,
                "uuid": "http://127.0.0.1/0298b509-2850-4dc0-ac11-b09ff5781b09",
                "orcid": "http://orcid.org/0000-0002-1825-0097",
                "givenName": "Ismail",
                "familyName": "Khennas",
                "gender": "male",
                "collaborators": [{'id': 2}],
                "outputs": [{'id': 1,
                             'title': "Africa needs context-relevant evidence to shape its clean energy future"}]
            },
        2:  {
                "id": 2,
                "uuid": "http://127.0.0.1/0298b509-2850-4dc0-ac11-b09ff5781b09",
                "orcid": "http://orcid.org/0000-0002-1825-0096",
                "givenName": "Isaah",
                "familyName": "Wally",
                "gender": "male",
                "collaborators": [{'id': 1}],
                "outputs": [{'id': 1,
                             'title': "Africa needs context-relevant evidence to shape its clean energy future"}]
                    },
        3:  {
                "id": 3,
                "uuid": "http://127.0.0.1/0298b509-2850-4dc0-ac11-b04hfy781b09",
                "orcid": "http://orcid.org/0000-0002-1825-0001",
                "givenName": "Blobby",
                "familyName": "MkFigus",
                "gender": "male",
                "collaborators": [],
                "outputs": [{'id': 2,
                             'title': "Potential Climate Change Risks to Meeting Zimbabwe’s NDC Goals and How to Become Resilient"}]
                     }
    }

    def get(self, id: int, collabs=False):
        if int(id) in self.authors:
            record = self.authors.get(int(id)).copy()
            print(record)

            if (collabs == True) and (record["collaborators"] is not None):
                print(record["collaborators"])
                filled = [self.authors.get(int(x['id'])) for x in record["collaborators"]]
                record["collaborators"] = filled
                return record
            else:
                record.pop("collaborators")
        else:
            raise KeyError("Author not found")


class OutputModel:
    def get(self, id: int):
        authors = AuthorModel()
        if id == 1:
            return {
                "id": 1,
                "year": 2022,
                "journal": "Nature Energy",
                "publisher": "Nature Publishing Group",
                "doi": "10.1038/s41560-022-01152-0",
                "title": "Africa needs context-relevant evidence to shape its clean energy future",
                "abstract": "Aligning development and climate goals means Africa’s energy systems will be based on clean energy technologies in the long term, but pathways to get there are uncertain and variable across countries. Although current debates about natural gas and renewables in Africa are heated, they largely ignore the substantial context specificity of the starting points, development objectives and uncertainties of each African country’s energy system trajectory. Here we—an interdisciplinary and majority African group of authors—highlight that each country faces a distinct solution space and set of uncertainties for using renewables or fossil fuels to meet its development objectives. For example, Ethiopia is headed for an accelerated green-growth pathway, but Mozambique is at a crossroads of natural gas expansion with implicit large-scale technological, economic, financial and social risks and uncertainties. We provide geopolitical, policy, finance and research recommendations to create firm country-specific evidence to identify adequate energy system pathways for development and to enable their implementation.",
                "authors": [authors.authors[1], authors.authors[2]]
            }
        elif id == 2:
            return {
                "id": 2,
                "year": 2021,
                "journal": "energies",
                "publisher": "MDPI",
                "doi": "10.3390/en14185827",
                "title": "Potential Climate Change Risks to Meeting Zimbabwe’s NDC Goals and How to Become Resilient",
                "abstract": "Almost all countries have committed to develop Nationally Determined Contributions (NDC) to reduce GHG emissions. They determine the level of GHG mitigation that, as a nation, they will commit to reducing. Zimbabwe has ambitious and laudable GHG mitigation targets. Compared to a coal-based future, emissions will be reduced by 33% per capita by 2030. If historical climate conditions continue, it can do this at low or negative cost if suitable sources of climate financing are in place. The NDC plots a positive future. However, much of Zimbabwe’s NDC mitigation center on hydropower generation and other measures that are dangerously vulnerable to climate change. Should the climate change in accordance with recent projections, these investments will be at risk, severely constraining electricity supply and causing high degrees of economic damage. This paper uses the Open-Source energy Modelling SYStem (OSeMOSYS) to consider two adaptation pathways that address this vulnerability. In the first, the country turns to a historically accessible option, namely the deployment of coal. In so doing, the electrical system is made more resilient, but emissions ramp up. The second pathway ‘climate proofs’ the power sector by boosting solar and wind capacity, using hydropower to provide balance for these new renewable resources, and introducing significant energy efficiency measures. This second pathway would require a set of extra accompanying investments and changes to the power market rules, but allows for both system resilience and NDC targets to be met. The paper shows that Zimbabwe’s low emissions growth can be made resilient, and while this path promises strong benefits, it also requires strong commitment and political will. From this paper insights are drawn and requirements for future analysis are made. Two critical insights are that: (i) NDCs that focus on mitigation should include resilience in their design. If they do not, they can introduce deep vulnerability; (ii) a departure from historical electricity market structures appears to hold potential for strong environmental, cost and reliability gains.",
                "authors": [authors.authors[3]]
            }