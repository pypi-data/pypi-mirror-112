from errors import TorchSdkException
from torch_sdk.models.pipeline import CreatePipeline
from torch_sdk.torch_http_client import TorchHttpClient
from torch_sdk.models.datasource import CreateDataSource


class TorchClient:
    """
            Description : Torch user client is used to send data to catalog server.

            :param url: (String) url of the catalog server
            :param timeout_ms: (Integer) timeout of the requests sending to catalog
            :param access_key: (String) Access key of API key. You can generate API key from torch UI's setting
            :param secret_key: (String) Secret key of API key.

            Ex.  TorchClient = TorchUserClient(url='https://torch.acceldata.local:5443', access_key='OY2VVIN2N6LJ', secret_key='da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
    """

    def __init__(self, url, timeout_ms=10000, access_key: str = None, secret_key: str = None):
        """
                Description : Torch user client is used to send data to catalog server.

                :param url: (String) url of the catalog server
                :param timeout_ms: (Integer) timeout of the requests sending to catalog
                :param access_key: (String) Access key of API key. You can generate API key from torch UI's setting
                :param secret_key: (String) Secret key of API key.

                Ex.  TorchClient = TorchUserClient(url='https://torch.acceldata.local:5443', access_key='OY2VVIN2N6LJ', secret_key='da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
        """

        if access_key is None and secret_key is None:
            raise Exception('Access key and secret key - required')
        self.client = TorchHttpClient(url=url, access_key=access_key, secret_key=secret_key, timeout_ms=timeout_ms)

    def create_pipeline(self, pipeline: CreatePipeline):
        """
        Description:
            To create pipeline in torch catalog service
        :param pipeline: (CreatePipeline) class instance of the pipeline to be created
        :return: (Pipeline) newly created pipeline class instance
        """
        if pipeline.uid is None or pipeline.name is None:
            raise Exception('To create a pipeline, pipeline uid/name is required')
        return self.client.create_pipeline(pipeline)

    def get_pipeline(self, uid: str):
        """
        Description:
            To get an existing pipeline from torch catalog
        :param uid: uid of the pipeline
        :return:(Pipeline) pipeline class instance
        """
        if uid is None:
            raise Exception('To get a pipeline, pipeline uid is required')
        return self.client.get_pipeline(uid)

    def create_datasource(self, datasource: CreateDataSource):
        """
        Description:
            To create datasource in torch catalog
        :param datasource: (CreateDataSource) class instance of the datasource to be created
        :return: (DataSource) newly created datasource
        """
        return self.client.create_datasource(datasource)

    def get_datasource(self, name: str):
        """
        Description:
            Find datasource by it's name in torch catalog
        :param name: name of the datasource given in torch
        :return: (DataSource) datasource
        """
        return self.client.get_datasource(name)

    def get_all_datasources(self):
        """
        Description:
            list all datasources in torch catalog
        :return: (DataSource) list of datasource
        """
        return self.client.get_all_datasources()

    def get_asset_types(self):
        """
        Description:
            get all asset types supported in torch catalog
        :return: list of asset types
        """
        return self.client.get_all_asset_types()

    def get_all_source_types(self):
        """
        Description:
            get all source types supported in torch catalog
        :return: list of all source type
        """
        return self.client.get_all_source_types()

    def get_property_templates(self):
        pass

    def get_connection_types(self):
        """
        Description:
            get all connection types supported in torch catalog
        :return: list of all connection types
        """
        return self.client.get_connection_types()

    def get_tags(self):
        return self.client.get_tags()

    def delete_tag(self, tag: str):
        return self.client.delete_tag(tag)

    def update_data_protection(self, tag: str, is_protected: bool):
        return self.client.update_data_protection(tag, is_protected)

    def discover(self):
        # add filters in discover api & more details in asset class
        return self.client.discover()

    def list_all_snapshots(self):
        return self.client.list_all_snapshots()

    def get_user(self, user_id = None, username = None):
        if user_id is None and username is None:
            raise TorchSdkException('Either provide uid or id to find an asset')
        if user_id is not None:
            return self.client.get_user_by_id(id=user_id)
        if username is not None:
            return self.client.get_user_by_name(username=username)

    def create_api_key(self):
        return self.client.create_api_keys()

    def get_api_keys(self):
        return self.client.get_api_keys()

    def delete_api_key(self, access_key: str):
        return self.client.delete_api_key(access_key)

    def get_notifications(self):
        return self.client.get_notifications()

    def get_incidents(self):
        return self.client.get_incidents()

    def list_all_analysis_pipelines(self):
        return self.client.list_all_analysis_pipelines()

    def get_analysis_pipeline(self, id: int):
        return self.client.get_analysis_pipeline(id)

    def get_all_auto_profile_configurations(self):
        return self.client.get_all_auto_profile_configurations()

    def get_asset(self, uid: str = None, id: int = None):
        """"
            Description:
                Find an asset of the datasource
            :param uid: (String) uid of the asset
            :param id: (Int) id of the asset in torch catalog
        """
        if uid is None and id is None:
            raise TorchSdkException('Either provide uid or id to find an asset')
        if uid is not None:
            return self.client.get_asset_by_uid(uid=uid)
        if id is not None:
            return self.client.get_asset_by_id(id=id)