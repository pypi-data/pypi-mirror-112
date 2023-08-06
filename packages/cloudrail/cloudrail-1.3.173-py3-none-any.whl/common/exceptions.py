class NotFoundException(Exception):
    pass


class UnsupportedCloudProviderException(Exception):
    def __init__(self, cloud_provider=None):
        if cloud_provider:
            super().__init__(f'Cloud provider {cloud_provider} is not supported')
        else:
            super().__init__()
