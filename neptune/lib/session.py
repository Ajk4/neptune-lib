from typing import Dict

from neptune.client.client import Client
from neptune.lib.credentials import Credentials
from neptune.lib.project import Project


class Session(object):
    def __init__(self, credentials: Credentials = Credentials.from_env()):
        """
        :param credentials: `Credentials` object for authenticating your calls to Neptune API.
        """
        self.credentials = credentials
        self._client = Client(credentials.api_address, credentials.api_token)

    def get_projects(self, namespace=None) -> Dict[str, Project]:
        """
        Retrieve projects from given namespace, that our available using given credentials.

        :param namespace: The default namespace is the one you declared when creating your API token.
        :return: A dictionary: project_name -> Project object
        """
        if namespace is None:
            namespace = self.credentials.namespace

        projects = [Project(self._client, p.id, namespace, p.name) for p in self._client.get_projects(namespace)]

        return dict((p.full_id, p) for p in projects)


def main():
    class FakeCreds(object):
        def __init__(self):
            self.api_address = 'https://app.neptune.ml/api'
            self.api_token = ''

    s = Session(FakeCreds())
    print('Session created.\n')

    projects = s.get_projects('neptune-ml')
    print('Projects: {}\n'.format(projects))

    project = projects['neptune-ml/Google-AI-Object-Detection-Challenge']
    members = project.get_members()
    print('Members: {}\n'.format(members))

    experiments = project.get_experiments()
    print('Experiments ({}): {}\n'.format(len(experiments), experiments))

    import pandas as pd
    with pd.option_context('display.max_rows', 10, 'display.max_columns', None, 'display.width', None):
        exp = experiments[16]
        print('System properties:\n{}\n'.format(exp.system_properties))
        print('Properties:\n{}\n'.format(exp.properties))
        print('Parameters:\n{}\n'.format(exp.parameters))
        print('Channels:\n{}\n'.format(exp.channels))

        leaderboard = project.get_leaderboard()
        print('Leaderboard:\n{}\n'.format(leaderboard))

    with pd.option_context('display.max_rows', 10, 'display.max_columns', None, 'display.width', None):
        channel_values = exp.get_numeric_channels_values('unet batch sum loss', 'unet epoch sum loss')
        print('Channel values:\n{}\n'.format(channel_values))


if __name__ == '__main__':
    main()
