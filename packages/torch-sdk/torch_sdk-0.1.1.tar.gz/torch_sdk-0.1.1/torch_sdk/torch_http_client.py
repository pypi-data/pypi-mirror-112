import logging
import time
from abc import ABC

import requests

from models.connection import ConnectionType, AnalysisPipeline
from models.notifications import Notification, Incident
from models.profile import AutoProfileConfiguration
from models.tags import TAG, Watch, AssetTag, AssetActivity, AssetComment, AssetLabel, User, APIKeys
from torch_sdk.errors import APIError, TorchSdkException
from torch_sdk.models.assetType import AssetType
from torch_sdk.models.datasource import CreateDataSource, DataSource, DatasourceSourceType, Crawler, RootAsset
from torch_sdk.models.job import Job
from torch_sdk.models.pipeline import CreatePipeline, Pipeline, PipelineRun
from torch_sdk.models.snapshot import SnapshotData
from torch_sdk.models.span import Span, SpanContextEvent, CreateSpanEvent
from torch_sdk.client import TorchClientInterFace
from torch_sdk.models.asset import Asset, AssetRelation, ChildAsset, Metadata

from dataclasses import asdict
import json

_HEADERS = {'User-Agent': 'Torch-sdk', 'accessKey': None, 'secretKey': None, 'Content-Type': 'application/json'}
catalog_api_path = "/catalog-server/api"
pipeline_api_path = "/torch-pipeline/api"

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TorchHttpClient(TorchClientInterFace, ABC):
    access_key = None
    secret_key = None
    logger = logging.getLogger('torch')
    logger.setLevel(logging.INFO)

    # Create torch client by passing secret and access keys of catalog server for a given url
    def __init__(self, url, timeout_ms=10000, access_key: str = None, secret_key: str = None):
        """
            Description : Torch client is used to send data to catalog server.

            :param url: (String) url of the catalog server
                        ex:  https://torch.acceldata.local:5443
            :param timeout_ms: (Integer) timeout of the requests sending to catalog
            :param access_key: (String) Access key of API key. You can generate API key from torch ui's setting
            :param secret_key: (String) Secret key of API key.

            : TorchClient = TorchClient(url='https://torch.acceldata.local:5443', access_key='OY2VVIN2N6LJ', secret_key='da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
        """
        self.timeout_ms = timeout_ms
        self._timeout = 10000
        self._catalog_api_base = f"{url}{catalog_api_path}"
        self._pipeline_api_base = f"{url}{pipeline_api_path}"
        if access_key is None and secret_key is None:
            raise Exception('Access key and secret key - required')
        self.access_key = access_key
        self.secret_key = secret_key
        _HEADERS['accessKey'] = access_key
        _HEADERS['secretKey'] = secret_key

    # # convert pipeline object to dict type
    def _convert_pipeline_to_dict(self, pipeline: CreatePipeline):
        """
        Description:
            Convert pipeline object to dict type.
        :param pipeline: createPipeline class instance
        :return: pipeline in dict type
        """
        pipeline_dict = pipeline.__dict__
        if pipeline.meta is not None:
            meta = asdict(pipeline.meta)
            pipeline_dict['meta'] = meta
        return pipeline_dict

    # function to create pipeline
    def create_pipeline(self, pipeline: CreatePipeline):
        """
        Description:
            Used to create pipeline
        :param pipeline: createPipeline class instance that you want to create
        :return: pipeline class instance
        """
        payload = self._convert_pipeline_to_dict(pipeline)
        pipeline_payload = {'pipeline': payload}
        response = self._put(
            f'{self._pipeline_api_base}/pipelines',
            payload=pipeline_payload
        )
        response['pipeline']['client'] = self
        self.logger.info('Pipeline Created')
        return Pipeline(**response['pipeline'])

    # get pipeline by uid
    def get_pipeline(self, uid: str):
        """
            Description:
                To get an existing pipeline from torch catalog
        :param uid: uid of the pipeline
        :return:(Pipeline) pipeline class instance
        """
        url = f'{self._pipeline_api_base}/pipelines/{uid}'
        response = self._get(url)
        response['pipeline']['client'] = self
        return Pipeline(**response['pipeline'])

    # to create job for any given pipeline
    def create_job(self, job: {}, pipelineId: int):
        """
        Description:
            Used to create job in a pipeline
        :param pipelineId: pipeline id of the respective pipeline
        :param job: createJob class instance that you want to add in pipeline
        :return: Job class instance of created job
        """
        response = self._put(
            f'{self._pipeline_api_base}/pipelines/{pipelineId}/jobs',
            payload=job
        )
        self.logger.info('Pipeline Job Created')
        return Job(**response['node'])

    # convert datasource to dict data type
    def _convert_datasource_to_dict(self, datasource: CreateDataSource):
        """
            Description:
                Convert CreateDataSource class instance to dict type
            :param datasource: CreateDataSource class instance
            :return: dict form of CreateDataSource class instance
        """
        payload = datasource.__dict__
        source_type = asdict(datasource.sourceType)
        payload['sourceType'] = source_type
        datasource_payload = {}
        if not datasource.isVirtual:
            config_prop = []
            for cp in datasource.configProperties:
                config_prop.append(asdict(cp))
            payload['properties'] = config_prop
        payload.pop('configProperties')
        datasource_payload['assembly'] = payload

        return datasource_payload

    # create datasource in torch
    def create_datasource(self, datasource: CreateDataSource):
        """
        Description:
            used to create datasource
        :param datasource: createDatasource class instance that you want to create
        :return: created datasource instance
        """
        payload = self._convert_datasource_to_dict(datasource)
        response = self._post(
            f'{self._catalog_api_base}/assemblies',
            payload=payload
        )
        response['data']['client'] = self
        return DataSource(**response['data'])

    def update_datasource(self, datasource_id: int, datasource: CreateDataSource):
        """
        Description:
            used to update datasource
        :param datasource_id: id of the datasource to be updated
        :param datasource: createDatasource class instance that you want to create
        :return: created datasource instance
        """
        payload = self._convert_datasource_to_dict(datasource)
        response = self._put(
            f'{self._catalog_api_base}/assemblies/{datasource_id}',
            payload=payload
        )
        response['data']['client'] = self
        return DataSource(**response['data'])

    def delete_datasource(self, datasource_id: int):
        """
        Description:
            used to delete datasource
        :param datasource_id: id of the datasource to be updated
        :return: response of the operation
        """
        response = self._delete(
            f'{self._catalog_api_base}/assemblies/{datasource_id}'
        )
        return response

    def get_root_asset(self, datasource_id):
        response = self._get(
            f'{self._catalog_api_base}/assemblies/{datasource_id}/rootAssets'
        )
        root_assets = list(response)
        root_assets_list = []
        for res in root_assets:
            root_assets_list.append(RootAsset(**res))
        return root_assets_list

    # to create asset for any given datasource
    def create_asset(self, asset: {}):
        """
        Description:
            Used to create asset in a datasource
        :param asset: (dict) asset input
        :return: Asset class instance of created asset
        """
        response = self._put(
            f'{self._catalog_api_base}/assets',
            payload=asset
        )
        response['data']['client'] = self
        return Asset(**response['data'])

    def start_crawler(self, datasource_name):
        response = self._post(
            f'{self._catalog_api_base}/crawler/{datasource_name}',
            payload={}
        )
        return Crawler(**response['data'])

    def restart_crawler(self, datasource_name):
        response = self._post(
            f'{self._catalog_api_base}/crawler/{datasource_name}/restart',
            payload={}
        )
        return Crawler(**response['data'])

    def remove_crawler(self, datasource_name):
        response = self._delete(
            f'{self._catalog_api_base}/crawler/{datasource_name}/restart'
        )
        return Crawler(**response['data'])

    def get_crawler_status(self, datasource_name):
        response = self._get(
            f'{self._catalog_api_base}/crawler/{datasource_name}',
        )
        return Crawler(**response['data'])

    # initialise new version of snapshot for a datasource
    def initialise_snapshot(self, snapshot_data: {}):
        """
        Description:
            Used to initialise new version of snapshot for a datasource
        :param snapshotData: dict of snapshotData class instance
        :return: created snapshotData class instance
        """
        response = self._post(
            f'{self._catalog_api_base}/snapshots/initialise',
            payload=snapshot_data
        )
        return SnapshotData(**response['data'])

    # get current version of datasource
    def get_current_snapshot(self, datasource_id: int):
        """
        Description:
            If you want to get current version of a datasource
        :param datasourceId: id of a datasource
        :return: SnapshotData class instance of datasource
        """
        response = self._get(
            f'{self._catalog_api_base}/snapshots/{datasource_id}/version'
        )
        return SnapshotData(**response)

    def list_datasource_snapshots(self, id: int):
        response = self._get(
            f'{self._catalog_api_base}/snapshots/{id}'
        )
        snapshots = list(response)
        snapshots_list = []
        for res in snapshots:
            snapshots_list.append(SnapshotData(**res))
        return snapshots_list

    def list_all_snapshots(self):
        response = self._get(
            f'{self._catalog_api_base}/snapshots'
        )
        snapshots = list(response)
        snapshots_list = []
        for res in snapshots:
            snapshots_list.append(SnapshotData(**res))
        return snapshots_list

    # create relation between asset
    def create_asset_relation(self, asset_relation: {}):
        """
        Description:
            used to create relation between any 2 existing assets
        :param asset_relation: relation dict object
        :return: created AssetRelation class instance
        """
        response = self._put(
            f'{self._catalog_api_base}/asset-relations',
            payload=asset_relation
        )
        return AssetRelation(**response['data'])

    # create run for a pipeline
    def create_pipeline_run(self, pipeline_run: {}):
        """
        Description:
            used to create a pipeline run
        :param pipeline_run:
        :return: pipelineRun class instance
        """
        pipelineId = pipeline_run['run']['pipelineId']
        response = self._post(
            f'{self._pipeline_api_base}/pipelines/{pipelineId}/runs',
            payload=pipeline_run
        )
        response['run']['client'] = self
        self.logger.info('Pipeline Run Created')
        return PipelineRun(**response['run'])

    # update run for a pipeline
    def update_pipeline_run(self, pipeline_run_id: int, pipeline_run: {}):
        """
        Description:
            used to update an existing pipeline run
        :param pipeline_run_id: pipeline run id that you want to update
        :param pipeline_run: pipelineRun class instance that you want to update
        :return: updated pipelineRun class instance
        """
        response = self._put(
            f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}',
            payload=pipeline_run
        )
        response['run']['client'] = self
        self.logger.info('Pipeline Run Updated')
        return PipelineRun(**response['run'])

    # get latest pipeline run
    def get_latest_pipeline_run(self, pipeline_id: int):
        """
            Description:
                To get latest pipeline run instance of any pipeline
        :param pipeline_id: id of the pipeline
        :return: PipelineRun instance
        """
        url = f'{self._pipeline_api_base}/pipelines/{pipeline_id}/latestRun'
        response = self._get(url)
        response['run']['client'] = self
        return PipelineRun(**response['run'])

    # create span for pipeline run
    def create_span(self, pipeline_run_id: int, span: dict):
        """
        Description:
            used to create span for any pipeline run
        :param pipeline_run_id:
        :param span: Span class instace
        :return: Span
        """
        response = self._post(
            f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}/spans',
            payload=span
        )
        self.logger.info('Span Created')
        return Span(**response['span'])

    def get_span(self, pipeline_run_id: int, uid: str):
        """
            Description:
                Get span of the pipeline run by uid
        :param pipeline_run_id: pipeline run id
        :param uid: uid of the span
        :return: SpanContext instance of the input span uid
        """
        url = f'{self._pipeline_api_base}/pipelines/runs/{pipeline_run_id}/spans/{uid}'
        response = self._get(url)
        response['span']['client'] = self
        return Span(**response['span'])

    # convert span object to dict type
    def convert_span_event_to_dict(self, span_event: CreateSpanEvent):
        """
            Description:
                Convert CreateSpanEvent class instance to dict type
            :param spanEvent: CreateSpanEvent class instance
            :return: dict form of CreateSpanEvent class instance
        """
        payload = span_event.__dict__
        # payload['eventUid'] = span_event.eventType
        event_payload = {'event': payload}
        return event_payload

    # create span event for any span
    def create_span_event(self, span_event: CreateSpanEvent):
        """
        Description:
            used to create span event
        :param span_event: CreateSpanEvent class instance that you want to create
        :return: SpanContextEvent class instance
        """
        payload = self.convert_span_event_to_dict(span_event)
        if span_event.spanId is None:
            Exception('To update a pipeline run, id is required.')
        response = self._post(
            f'{self._pipeline_api_base}/pipelines/spans/{span_event.spanId}/events',
            payload=payload
        )
        self.logger.info('Span Event Created')
        return SpanContextEvent(**response['event'])

    def get_all_asset_types(self):
        """
        Description:
            get all asset types supported in torch xatalog
        :return: list of asset types
        """
        response = self._get(
            f'{self._catalog_api_base}/asset-types'
        )
        asset_types = list(response['data'])
        asset_types_res = []
        for res in asset_types:
            asset_types_res.append(AssetType(**res))
        return asset_types_res

    def get_all_source_types(self):
        """
        Description:
            get all source types supported in torch catalog
        :return: list of all source type
        """
        response = self._get(
            f'{self._catalog_api_base}/source-types'
        )
        source_types = list(response['data'])
        source_types_res = []
        for res in source_types:
            source_types_res.append(DatasourceSourceType(**res))
        return source_types_res

    def get_connection_types(self):
        """
        Description:
            get all source types supported in torch catalog
        :return: list of all source type
        """
        response = self._get(
            f'{self._catalog_api_base}/connection-types'
        )
        connection_types = list(response['data'])
        conn_type_response = []
        for res in connection_types:
            conn_type_response.append(ConnectionType(**res))
        return conn_type_response

    def get_tags(self):
        response = self._get(
            f'{self._catalog_api_base}/assets/tags'
        )
        tags = list(response['tags'])
        tags_list = []
        for res in tags:
            tags_list.append(TAG(**res))
        return tags_list

    def delete_tag(self, tag):
        tags = self.get_tags()
        tag_id = None
        for tg in tags:
            if tg.name == tag:
                tag_id = tg.id
        if tag_id is None:
            raise TorchSdkException(f'Tag not found with name {tag}')
        response = self._delete(
            url=f'{self._catalog_api_base}/tag/{tag_id}'
        )
        return response

    def update_data_protection(self, tag: str, is_protected: bool):
        payload = {
            'isProtected': is_protected
        }
        tags = self.get_tags()
        tag_id = None
        for tg in tags:
            if tg.name == tag:
                tag_id = tg.id
        if tag_id is None:
            raise TorchSdkException(f'Tag not found with name {tag}')
        response = self._put(
            url=f'{self._catalog_api_base}/tags/{tag_id}',
            payload=payload
        )
        return response

    def discover(self):
        url = f'{self._catalog_api_base}/assets/discover?page=0&size=25'
        response = self._get(url)
        datasource = list(response['data']['assemblies'])
        ds_list = []
        for res in datasource:
            ds_list.append(DataSource(**res))

        assets = list(response['data']['assets'])
        assets_list = []
        for res in assets:
            assets_list.append(Asset(**res))
        response = {
            'datasources': ds_list,
            'assets': assets_list
        }
        return response

    def get_datasource(self, name: str):
        """
        Description:
            Find datasource by it's name in torch catalog
        :param name: name of the datasource given in torch
        :return: (DataSource) datasource
        """
        if name is None:
            raise Exception('DataSource name is required')
        url = f'{self._catalog_api_base}/assemblies?name={name}'
        response = self._get(url)
        datasource = list(response['data'])
        if len(datasource) > 0:
            datasource[0]['client'] = self
            return DataSource(**datasource[0])
        raise Exception('datasource not found.')

    def get_all_datasources(self):
        """
        Description:
            list all datasources in torch catalog
        :return: (DataSource) list of datasource
        """
        url = f'{self._catalog_api_base}/assemblies'
        response = self._get(url)
        datasources = list(response['data'])
        ds_list = []
        for res in datasources:
            ds_list.append(DataSource(**res))
        return ds_list

    def get_asset_by_id(self, id: int):
        """
        Description:
            used to find an asset
        :param id: id of an asset
        :return: asset data (Asset)
        """
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets?ids={id}'
        asset = self._get_asset(url)
        asset_res = list(asset['data'])[0]
        asset_res['client'] = self
        return Asset(**asset_res)

    def get_asset_by_uid(self, uid: str):
        """
        Description:
            used to find an asset
        :param uid: uid of an asset
        :return: asset data (Asset)
        """
        if uid is None:
            raise Exception('Asset uid is required')
        url = f'{self._catalog_api_base}/assets?uid={uid}'
        asset = self._get_asset(url)
        asset['data']['client'] = self
        return Asset(**asset['data'])

    def _get_asset(self, url: str):
        response = self._get(
            url=url
        )
        return response

    def delete_asset(self, id: int):
        response = self._delete(
            url=f'{self._catalog_api_base}/assets/{id}'
        )
        return response

    def get_asset_metadata(self, id: int):
        url = f'{self._catalog_api_base}/assets/{id}/metadata'
        response = self._get(
            url=url
        )
        metadata = Metadata(**response['data'])
        return metadata

    def update_asset_metadata(self, id: int, metadata: dict):
        url = f'{self._catalog_api_base}/assets/{id}/metadata'
        response = self._put(
            url=url,
            payload= metadata
        )
        metadata = Metadata(**response['data'])
        return metadata

    def get_related_assets(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/relatedAssets'
        response = self._get(
            url=url
        )
        relations = list(response['relations'])
        relations_list = []
        for res in relations:
            relations_list.append(AssetRelation(**res))
        return relations_list

    def get_child_assets(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/childAssets'
        response = self._get(
            url=url
        )
        child_assets = list(response['childAssets'])
        child_assets_list = []
        for res in child_assets:
            child_assets_list.append(ChildAsset(**res))
        return child_assets_list

    def start_watch(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/watch'
        response = self._post(
            url=url
        )
        start_watch = Watch(**response['data'])
        return start_watch

    def stop_watch(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/watch'
        response = self._delete(
            url=url
        )
        return response

    def get_asset_tags(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/tags'
        response = self._get(
            url=url
        )
        tags = list(response['assetTags'])
        tags_list = []
        for res in tags:
            tags_list.append(AssetTag(**res))
        return tags_list

    def add_asset_tag(self, id: int, payload: dict):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/tag'
        response = self._post(
            url=url, payload=payload
        )
        return AssetTag(**response)

    def remove_asset_tag(self, id: int, tag_id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/removeTag/{tag_id}'
        response = self._delete(
            url=url
        )
        return response

    def add_asset_labels(self, id: int, payload: dict):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/labels'
        response = self._put(
            url=url, payload=payload
        )
        labels = list(response)
        labels_list = []
        for lbl in labels:
            labels_list.append(AssetLabel(**lbl))
        return labels_list

    def get_asset_labels(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/labels'
        response = self._get(
            url=url
        )
        labels = list(response)
        labels_list = []
        for lbl in labels:
            labels_list.append(AssetLabel(**lbl))
        return labels_list

    def update_asset_annotation(self, id: int, payload: dict):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/annotation'
        response = self._put(
            url=url, payload=payload
        )
        return response

    def get_asset_activity(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/activity'
        response = self._get(
            url=url
        )
        return AssetActivity(**response)

    def get_asset_comment(self, id: int):
        if id is None:
            raise Exception('Asset id is required')
        url = f'{self._catalog_api_base}/assets/{id}/comments'
        response = self._get(
            url=url
        )
        comments = list(response['comments'])
        comments_list = []
        for res in comments:
            comments_list.append(AssetComment(**res))
        return comments_list

    def get_user_by_id(self, id: int):
        if id is None:
            raise TorchSdkException('User id is required')
        url = f'{self._catalog_api_base}/user/{id}'
        response = self._get(
            url=url
        )
        return User(**response)

    def get_user_by_name(self, username: int):
        if id is None:
            raise TorchSdkException('Username is required')
        url = f'{self._catalog_api_base}/user/byname/{username}'
        response = self._get(
            url=url
        )
        return User(**response)

    def list_all_analysis_pipelines(self):
        response = self._get(
            url=f'{self._catalog_api_base}/analytics-pipelines'
        )
        keys = list(response['pipelines'])
        keys_list = []
        for res in keys:
            keys_list.append(AnalysisPipeline(**res))
        return keys_list

    def get_analysis_pipeline(self, id: int):
        response = self._get(
            url=f'{self._catalog_api_base}/analytics-pipelines/{id}'
        )
        return AnalysisPipeline(**response['pipeline'])

    def get_all_auto_profile_configurations(self):
        response = self._get(
            url=f'{self._catalog_api_base}/assemblies/auto-profile-configurations'
        )
        configs = list(response)
        auto_profile_list = []
        for res in configs:
            auto_profile_list.append(AutoProfileConfiguration(**res))
        return auto_profile_list

    def get_auto_profile_configuration(self, datasource_id: int):
        response = self._get(
            url=f'{self._catalog_api_base}/assemblies/{datasource_id}/auto-profile-configuration'
        )
        return AutoProfileConfiguration(**response)

    def remove_auto_profile_configuration(self, datasource_id: int):
        response = self._delete(
            url=f'{self._catalog_api_base}/assemblies/{datasource_id}/auto-profile-configuration'
        )
        return response

    def create_api_keys(self):
        response = self._post(
            url=f'{self._catalog_api_base}/key'
        )
        return APIKeys(**response['data'])

    def get_api_keys(self):
        response = self._get(
            url=f'{self._catalog_api_base}/key'
        )
        keys = list(response['apiKeys'])
        keys_list = []
        for res in keys:
            keys_list.append(APIKeys(**res))
        return keys_list

    def delete_api_key(self, access_key: str):
        list = self.get_api_keys()
        access_key_id = None
        for i in list:
            if i.accessKey == access_key:
                access_key_id = i.id
        if access_key_id is None:
            raise TorchSdkException(f'Access key {access_key} not found in torch catalog.')
        response = self._delete(
            url=f'{self._catalog_api_base}/key/{access_key_id}'
        )
        return response

    def get_notifications(self):
        response = self._get(
            url=f'{self._catalog_api_base}/notifications?page=0&size=50&sortBy=id:DESC'
        )
        notifications = list(response['notification'])
        notifications_list = []
        for res in notifications:
            notifications_list.append(Notification(**res))
        return notifications_list

    def get_incidents(self):
        response = self._get(
            url=f'{self._catalog_api_base}/incidents'
        )
        incidents = list(response['incidents'])
        inc_list = []
        for res in incidents:
            inc_list.append(Incident(**res))
        return inc_list

    @staticmethod
    def now_ms():
        return int(round(time.time() * 1000))

    def _post(self, url, payload=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.post(
            url=url, headers=_HEADERS, json=payload, timeout=self._timeout, verify=False
        )
        self.logger.info(
            f" POST {url} "
            f"payload={json.dumps(payload)} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _put(self, url, payload=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.put(
            url=url, headers=_HEADERS, json=payload, timeout=self._timeout, verify=False
        )
        self.logger.info(
            f" PUT {url} "
            f"payload={json.dumps(payload)} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _get(self, url, params=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.get(
            url=url, params=params, headers=_HEADERS, timeout=self._timeout, verify=False
        )
        self.logger.info(
            f" GET {url} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return self._response(response, as_json)

    def _delete(self, url, params=None, as_json=True):
        now_ms = self.now_ms()
        if _HEADERS['accessKey'] is None:
            _HEADERS['accessKey'] = self.access_key
        if _HEADERS['secretKey'] is None:
            _HEADERS['secretKey'] = self.secret_key
        response = requests.delete(
            url=url, params=params, headers=_HEADERS, timeout=self._timeout, verify=False
        )
        self.logger.info(
            f" DELETE {url} "
            f"duration_ms={self.now_ms() - now_ms}"
        )

        return response

    def _response(self, response, as_json):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f' {response.text}')
            self._raise_api_error(e)

        return response.json() if as_json else response.text

    def _raise_api_error(self, e):
        raise APIError() from e
