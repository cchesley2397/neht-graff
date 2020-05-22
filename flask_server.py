from flask import Flask, request, render_template, jsonify, g
from neo4j import GraphDatabase, basic_auth, CypherError
from os import environ
from utils import query_result_parsing, cypher_refactoring, io
from config import Config

config = Config('./config.json')

# Flask Configuration
FLASK_PORT = config.get_val('flask_port')

# Neo4j Configuration
NEO4J_URI = config.get_val('neo4j_uri')
NEO4J_CREDS = (environ['NEO4J_USER'], environ['NEO4J_PASSWORD'])


app = Flask(__name__, template_folder='./templates')


def get_db():
    if 'db' not in g:
        g.db = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(user=NEO4J_CREDS[0], password=NEO4J_CREDS[1]), encrypted=False)
    return g.db


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def submit(query):
    """
    Submits the specified query using a driver representing an established connection to a neo4j database
    Catches errors for blank queries and invalid Cypher syntax
    :param query: String containing a Cypher query
    :return: Iterable of 1 or more Neo4j records
    """

    if not query:
        return 'Query is null.', 1, ''
    elif query == '':
        return 'Query is blank', 2, ''
    else:
        try:
            driver = get_db()
            with driver.session() as session:
                result = session.run(query)
                return result, 0, ''
        except CypherError as e:
            return 'Query is invalid', 3, e.message
        finally:
            close_db()


@app.route('/set_directory', methods=['GET', 'POST'])
def set_directory():
    if request.method == 'GET':
        if config.has_val('log_path'):
            return render_template('./set_directory.html', default=config.get_val('log_path'))
        else:
            return render_template('./set_directory.html', default='./data/zeek')
    elif request.method == 'POST':
        log_path = request.form['log_path']
        config.set_val('log_path', log_path)
        # TODO check for existence of directory
        if config.has_val('start_time') and config.has_val('end_time'):
            render_template('graph.html')
        else:
            render_template('set_time.html')
            # TODO add time selection
        return render_template('graph.html')
    else:
        return 'Method not accepted.'


# GET response: render graph.html
# POST response: submit search bar query to specified DB, then render graph.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if config.has_val('log_path'):
        if request.method == 'POST':
            refactored_query = cypher_refactoring.refactor_query(request.form['query'])
            print('Refactored query: ', refactored_query)
            result, code, message = submit(refactored_query)
            if code == 0:
                records_json = query_result_parsing.parse_records(result)
                return render_template('./graph.html', json_data=records_json, error='Enter query: ')
            else:
                print('ERROR: ' + str(message))
                return render_template('./graph.html', error=result, message=message)
        else:
            return render_template('./graph.html')
    else:
        if config.has_val('log_path'):
            return render_template('./set_directory.html', default=config.get_val('log_path'))
        else:
            return render_template('./set_directory.html', default='./data/zeek')


@app.route('/submit_query', methods=['POST'])
def query_pivot():
    query = request.get_json()
    query = cypher_refactoring.refactor_query(query)
    result, code, message = submit(query)
    if code == 0:
        result_json = query_result_parsing.parse_records(result)
        return jsonify(result_json)
    else:
        print('ERROR: ' + str(message))
        return jsonify(message)


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
