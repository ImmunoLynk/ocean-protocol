'''Core module for metadata related operations'''

import requests
import hashlib
import datetime

import flask

def get_metadata(
    request_json
):
    '''Utility function to get define an asset metadata.'''    

    r = requests.post(
        request_json['ipfs']['endpoint'] + '/retrieve',
        data=flask.jsonify({
            'user': request_json.get('publisher').get('address'),
            'hash': request_json['ipfs'].get('hash'),
            'type': request_json['ipfs'].get('type'),
        })
    )
    test_data = r.json()
    q_data = test_data['questionnaire']
    img_data = test_data['image']
    
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    price = str(request_json['price'])
    
    metadata = {
        'main': {
            'name': 'ImmunoLynk test result',
            'type': 'dataset',
            'dateCreated': datetime.datetime.now().strftime(datetime_format),
            'author': 'ImmunoLynk',
            'license': 'MIT LICENSE', # TODO: is this license correct?
            'price': price,
            'files': [
                {
                    'url': q_data['link'],
                    'name': q_data['id'],
                    'index': 0,
                    'contentType': 'text/' + q_data['type'],
                    'checksum': hashlib.md5(q_data['id']).hexdigest(),
                    'checksumType': 'MD5',
                    'contentLength': q_data['Size'],
                },
                {
                    'url': img_data['link'],
                    'name': img_data['id'],
                    'index': 1,
                    'contentType': 'image/' + img_data['type'], # what goes in here?
                    'checksum': hashlib.md5(img_data['id']).hexdigest(),
                    'checksumType': 'MD5',
                    'contentLength': img_data['Size'],
                }
            ],
        }
    }
    
    return metadata
