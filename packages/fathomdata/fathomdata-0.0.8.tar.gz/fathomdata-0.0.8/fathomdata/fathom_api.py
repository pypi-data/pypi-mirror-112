import requests
from requests.exceptions import HTTPError
import pandas as pd


from .document import Document

__fathom_state = {
    'environment': 'demo',
    'api_key': None,
    'important_document_columns': [
        'DocumentId',
        'ReceivedTime',
        'Source',
        #'ContentType',
        'Filename',
        'UploadedByUserId',
        #'IsValidated'
    ],
    'document_cache': {}
}


def set_api_key(api_key):
    __fathom_state['api_key'] = api_key


def _set_environment(environment):
    __fathom_state['environment'] = environment


def available_documents(document_type='batch'):

    if document_type == 'batch':

        url = __get_endpoint('record')
        headers = __get_request_headers()

        response = __handle_api_request("get", url, headers=headers)

        dataframe = pd.DataFrame.from_dict(response.json())
        dataframe = dataframe[__fathom_state['important_document_columns']]
        dataframe['ReceivedTime'] = pd.to_datetime(dataframe['ReceivedTime'])
        return dataframe

    return None


def get_document(document_id, document_type='processed'):

    if not document_id in __fathom_state['document_cache']:
        __fathom_state['document_cache'][document_id] = {}

    if not document_type in __fathom_state['document_cache'][document_id]:

        url = f"{__get_endpoint('record')}/{document_id}/{document_type}"
        headers = __get_request_headers()

        response = __handle_api_request("get", url, headers=headers)
        __fathom_state['document_cache'][document_id][document_type] = response.json()

    document_data = __fathom_state['document_cache'][document_id][document_type]
    return Document(document_data, document_id)


def ingest_document(path=None, filename=None, content=None, document_category=None):

    if bool(path) == bool(content): #xor
        raise ValueError("Specify either path or content, but not both")
    elif not filename and not path:
        raise ValueError("Must specify a filename or path")
    
    filename = filename or path.split('/')[-1]
    filecontent = content or open(path, "rb")

    query_parameters = {
        'filename': filename,
        'documentCategory': document_category
    }

    upload_url = __get_endpoint("upload")
    headers = __get_request_headers()
    
    fathom_response = __handle_api_request("get", upload_url, headers=headers, params=query_parameters)

    fathom_response_data = fathom_response.json()
    s3_fields_data = fathom_response_data['fields']
    new_document_key = fathom_response_data['fields']['key']
    presigned_link_url = fathom_response_data['url']
    files={"file": (filename, filecontent, "application/pdf")}

    __handle_api_request("post", presigned_link_url, data=s3_fields_data, files=files)

    return new_document_key

def __get_endpoint(endpoint):
    return f"{__get_api_base_url()}/{endpoint}"

def __get_api_base_url():

    if __fathom_state['environment'] in ['demo', 'staging']:
        return f"https://{__fathom_state['environment']}.api.fathom.one"
    else:
        return f"https://{__fathom_state['environment']}.execute-api.us-east-1.amazonaws.com/dev"

def __get_request_headers():

    return {
        'x-api-key': __fathom_state['api_key']
    }

def __handle_api_request(method, url, **kwargs):
    
    #pass through fathom api error messages instead of http reasons
    if method.lower() not in ["get", "post"]:
        raise Exception("Unsupported method: must be either GET or POST")

    response = requests.request(method, url, **kwargs)

    if 400 <= response.status_code < 600:
        message = response.json().get("message")
        raise HTTPError(f"{response.status_code} {response.reason}: {message}", response=response)

    return response
