from Return import Return
from Arg import Arg
from Route import Route
from Signature import Signature
from Docstring import Docstring
import json
import os


fi = 'app.py' # the default file for path / methods


def obtain_signatures() -> list:
    file = open(fi, 'r')
    content = file.read()
    fun = content.split('\n')
    sigs = []
    for f in fun:
        if 'def ' in f and '#' not in f:
            sigs.append(Signature(f))
    return sigs


def obtain_routes() -> list:
    file = open(fi, 'r')
    content = file.read()
    lines = content.split('\n')  # get all lines
    routes = []
    for l in lines:
        if '@app.route' in l and '#' not in l:  # if there is the decorator not commented
            routes.append(Route(l))
    return routes


def obtain_all_docstrings(objects_path: str) -> list:
    li = []
    for path in os.listdir(objects_path):
        if path[:2] != '__':
            li.append(obtain_docstring(os.path.join(objects_path, path)))
    return li


def obtain_docstring(file_path: str) -> list:
    """Parse file to obtain docstrings

    Args:
        file_path (str): the path of the file to parse

    Returns:
        list[Docstring]: all the dosctrings inside the file
    """
    file = open(file_path, 'r')
    content = file.read()
    docs = content.split('\"\"\"')
    li = []
    for i in range(len(docs)):
        if i % 2 == 1:
            li.append(
                Docstring(docs[i], file_path.split('/')[-1].split('.py')[0]))
    return li


def couple_route_signature(routes: list, signatures: list) -> list:
    """[summary]

    Args:
        routes (list): [description]
        signatures (list): [description]

    Returns:
        list: [description]
    """
    couples = []
    if len(routes) != len(signatures):
        print(f'{len(routes)} routes not matching {len(signatures)} methods')
        return couples
    for i in range(len(routes)):
        couples.append((routes[i], signatures[i]))
    return couples


'''
def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def generate_imported_objects(objects_path: str) -> list:
    li = []
    for obj in os.listdir(objects_path):
        if obj[:2] != '__':
            imp = f'{objects_path}.{obj[:-3]}.{obj[:-3]}'
            # print('[', obj, ']', imp, '\n')
            li.append(get_class(imp)(''))
    return li
'''

def identify_type(arg: Arg):
    object_type = arg.type
    name = arg.name
    prop = {"type": "str"}
    if object_type == 'str':
        prop['type'] = 'string'
        prop['example'] = 'hello there'
    elif object_type == 'dict':
        prop['type'] = 'string'
        prop['example'] = '{\'key\': \'value\'}'
    elif object_type == 'int':
        prop['type'] = 'integer'
        prop['example'] = 314
    elif object_type == 'float':
        prop['type'] = 'float'
        prop['example'] = 3.1415
    elif object_type == 'bool':
        prop['type'] = 'boolean'
        prop['example'] = True
    # TODO manage object and array type
    elif 'list' in object_type:
        prop['type'] = 'array'
        prop['items'] = identify_type(arg.arg)
    else:  # object
        # prop['type'] = 'object'
        # prop['OneOf'] = {"$ref": f"{object_type}.json"}
        prop = {"$ref": f"{object_type.lower()}.json"}

    # print(object_type, prop)
    return prop


def from_rawstr_to_type(return_object: Return) -> str:
    if 'list' in return_object.type:
        return from_rawstr_to_type(return_object.arg)
    elif return_object.type == 'dict':
        return 'str'
    else:
        return return_object.type


def generate_schema(docstring: Docstring):
    if docstring is not []:
        schema = {"type": "object",
                  "required": [],
                  "properties": [],
                  }
        required = []
        properties = {}
        for att in docstring.att:  # for each attribute in the docstring's attributes
            properties[att.name] = identify_type(att)
            required.append(att.name)
        schema["required"] = required
        schema["properties"] = properties
        # print(att.name, att.type, f_name)
        f_name = f'swagger/schemas/core/{docstring.name.lower()}.json'

        # if the file already exists we don't want to overwrite it
        # we write if it doesn't exist
        if os.path.exists(os.path.join(os.getcwd(), f_name)) is False:
            f = open(f_name, 'w')
            json.dump(schema, f, indent=2)
            print(f'\t\033[92m + file {f_name}\033[0m')
            f.close()
        else: 
            print(f'\t\033[90m ~ file {f_name}\033[0m')


def generate_schemas(file_path: str):
    print(f'Generation of objects schemas in {file_path}')
    # verifiy if folder swagger exists
    if os.path.exists(os.path.join(os.getcwd(), 'swagger')) is False:
        os.mkdir(os.path.join(os.getcwd(), 'swagger'))
        os.mkdir(os.path.join(os.getcwd(), 'swagger', 'schemas'))
        os.mkdir(os.path.join(os.getcwd(), 'swagger', 'schemas', 'core'))
        os.mkdir(os.path.join(os.getcwd(), 'swagger', 'schemas', 'errors'))
    # verify if swagger/schemas exists
    if os.path.exists(os.path.join(os.getcwd(), 'swagger', 'schemas')) == False:
        os.mkdir(os.path.join(os.getcwd(), 'swagger', 'schemas'))
        if os.path.exists(os.path.join(os.getcwd(), 'swagger', 'schemas', 'core')) is False:
            os.mkdir(os.path.join(os.getcwd(), 'swagger', 'schemas', 'core'))
        elif os.path.exists(os.path.join(os.getcwd(), 'swagger', 'schemas', 'errors')) is False:
            os.mkdir(os.path.join(os.getcwd(), 'swagger', 'schemas', 'errors'))

    docstrings = obtain_all_docstrings(file_path)
    # print(docstrings)
    for files in docstrings:
        for doc in files:
            generate_schema(doc)

    # error 404 default
    f = open(f'swagger/schemas/errors/404.json', 'w')
    json.dump(generate_response_404(), f, indent=2)
    f.close()
    # generate_primordial_types()


def generate_primordial_types():
    """Generate primordial types shcemas
    """
    # str
    f = open(f'swagger/schemas/core/str.json', 'w')
    json.dump({'type': 'string', 'example': 'hello there'}, f, indent=2)
    f.close()
    # int
    f = open(f'swagger/schemas/core/int.json', 'w')
    json.dump({'type': 'int', 'example': 31415}, f, indent=2)
    f.close()
    # float
    f = open(f'swagger/schemas/core/float.json', 'w')
    json.dump({'type': 'float', 'example': 3.1415926535}, f, indent=2)
    f.close()
    # bool
    f = open(f'swagger/schemas/core/bool.json', 'w')
    json.dump({'type': 'boolean', 'example': True}, f, indent=2)
    f.close()


def is_primordial(object_type: str) -> str:
    if object_type == 'str' or object_type == 'int' or object_type == 'float' or object_type == 'bool' or object_type == 'dict':
        return True
    else:
        return False


def file_name(arg: Arg) -> str:
    if arg.arg is not None:
        return file_name(arg.arg)
    else:
        return f'swagger/schemas/core/{arg.type}.json'


def generate_response_200(signature: Signature) -> dict:
    if signature.ret.type == '':
        resp = {
            "description": "200 response"
        }
        return resp
    elif signature.ret.arg is not None:
        resp = {
            "description": "200 response",
            "schema": {
                "$ref": f"swagger/schemas/core/{from_rawstr_to_type(signature.ret).lower()}.json"
            }
        }
    else:
        resp = {
            "description": "200 response",
            "schema": {
                "$ref": f"swagger/schemas/core/{signature.ret.type.lower()}.json"
            }
        }
    return resp


def generate_response_404() -> dict:
    """Generate a default 404 template

    Returns:
        dict: the template
    """
    not_found = {"type": "object",
                 "properties": {
                     "code": {
                         "type": "string",
                         "example": 404
                     },
                     "message": {
                         "type": "string",
                         "example": "not found"
                     }
                 }
                 }
    return not_found


def generate_path(couples: list) -> dict:
    """ Generate the main swagger file based
        on the couples list

    Args:
        couples (list): tuple route / signature

    Returns:
        dict: the newly created json object
    """
    json = {}
    for couple in couples:
        route = couple[0]
        signature = couple[1]
        nb_method = len(route.methods)
        if nb_method > 0:
            json[route.path] = {}
        summary = "empty"  # TODO generate docstring
        for method in route.methods:
            json[route.path][method.lower()] = {
                "responses": {
                    "200": generate_response_200(signature),
                    "404": {
                        "description": "not found",
                        "schema": {
                            "$ref": "swagger/schemas/errors/404.json"
                        }
                    }
                },
                "summary": summary,
                "parameters": [
                ]
            }
            for a in signature.args:
                if a.type == "str":
                    x = "string"
                else:
                    x = a.type
                json[route.path][method.lower()]['parameters'].append(
                    {"name": a.name,
                     "in": "path",
                     "required": True,
                     "type": x,
                     "description": "Docstring"
                     })

    return json


def generate_open_api():
    # schemas generation
    generate_schemas('Objects')
    generate_primordial_types()

    # files parsing
    rou = obtain_routes()
    sig = obtain_docstring(fi)
    cou = couple_route_signature(rou, sig)

    host = "petstore.swagger.io"  # default

    # look for a .chalice folder
    if '.chalice' in os.listdir(os.path.join('.')):
        path = os.path.join('.chalice', 'deployed', 'ew1.json')
        j = json.load(open(path, 'r'))
        for r in j.get('resources'):
            if r.get('name') == 'rest_api':
                host = r.get('rest_api_url').split('//')[1].split('/')[0]


    file = {"swagger": "2.0",
            "info": {
                "version": "1.0.0",
                "title": "Auto generated",
                "license": {
                    "name": "MIT"
                }
            },
            "host": host,
            "basePath": "/v1",
            "schemes": [
                "http"
            ],
            "consumes": [
                "application/json"
            ],
            "produces": [
                "application/json"
            ],
            "paths": generate_path(cou)
            }

    example = open('swagger.json', 'w')
    json.dump(file, example, indent=2)

# generate_open_api()
if __name__ == "__main__":
    # execute only if run as a script
    print('hello there')