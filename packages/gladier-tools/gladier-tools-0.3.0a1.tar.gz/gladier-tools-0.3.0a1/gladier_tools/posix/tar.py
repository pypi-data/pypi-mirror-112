from gladier import GladierBaseTool, generate_flow_definition


def tar(**data):
    import os
    import tarfile
    import pathlib
    tar_input = data['tar_input']
    
    if '~' in tar_input:
        tar_input = os.path.expanduser(tar_input)
        
    path = pathlib.PurePath(tar_input)
    os.chdir(path.parent)

    tar_output = data.get('tar_output', f'{tar_input}.tgz')
    with tarfile.open(tar_output, 'w:gz') as tf:
        tf.add(path.name)
            
    return tar_output


class Tar(GladierBaseTool):

    # Custom flow definition to set 'ExceptionOnActionFailure' to True. We don't
    # want a transfer to start if tarring fails
    flow_definition = {
        'Comment': 'Flow with states: Tar a given folder',
        'StartAt': 'Tar',
        'States': {
            'Tar': {
                'ActionUrl': 'https://automate.funcx.org',
                'ActionScope': 'https://auth.globus.org/scopes/b3db7e59-a6f1-4947-95c2-59d6b7a70f8c/action_all',
                'Comment': None,
                'ExceptionOnActionFailure': True,
                'Parameters': {
                    'tasks': [
                        {
                            'endpoint.$': '$.input.funcx_endpoint_compute',
                            'function.$': '$.input.tar_funcx_id',
                            'payload.$': '$.input'
                        }
                    ]
                },
                'ResultPath': '$.Tar',
                'Type': 'Action',
                'WaitTime': 300,
                'End': True,
            },
        }
    }

    funcx_functions = [tar]
    required_input = [
        'tar_input', 
        'funcx_endpoint_compute'
        ]
