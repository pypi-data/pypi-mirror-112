from torch_sdk.models.create_asset import AssetMetadata
from torch_client import TorchClient
from torch_sdk.models.datasource import CreateDataSource, SourceType, ConfigProperty

torch_client = TorchClient(url="https://torch.acceldata.local:5443",
                           access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

# get connection types
# connection_types = torch_client.get_connection_types()
# print(connection_types)

# get tags defined in torch, update protection flag, delete tag
# tags = torch_client.get_tags()
# print(tags)
# torch_client.update_data_protection(tag='asset_tag', is_protected=True)
# torch_client.delete_tag(tag='asset_tag')


# get related assets and child assets
# datasource = torch_client.get_datasource('postgres_ds_local')
# asset = datasource.get_asset(id=20)
# relations = asset.get_related_assets()
# print(relations)
# child_assets = asset.get_child_assets()
# print(child_assets)

# discover
# discover_res = torch_client.discover()
# print(discover_res)

# watch asset
# start_watch = asset.start_watch()
# print(start_watch)
# asset.stop_watch()

# tags
# tags = asset.get_asset_tags()
# print(tags)
# tag_add = asset.add_asset_tag(tag='asset_tag')
# print(tag_add)
# tag_rm = asset.remove_asset_tag(tag='asset_tag')
# print(tag_rm)


# asset activty
# activty = asset.get_asset_activity()
# print(activty)

# asset comment
# comments = asset.get_asset_comment()
# print(comments)

# labels
# labels = asset.add_asset_labels(labels = ['teamtorch', 'comp:adinc'])
# print(labels)
# labels = asset.get_asset_labels()
# print(labels)

# annotation
# annotation = asset.update_asset_annotation(annotation='this asset is created and accessed from torch sdk')
# print(annotation)

# delete an asset
# datasource.delete_asset(id=9523)

# list all snapshots
# snapshots = datasource.list_all_snapshots()
# print(snapshots)
# snapshots = torch_client.list_all_snapshots()
# print(snapshots)

# get user
# user = torch_client.get_user(user_id=3)
# print(user)
# user = torch_client.get_user(username='admin')
# print(user)

# crawler
# datasource.start_crawler()
# datasource.get_crawler_status()
# datasource.restart_crawler()

# api keys
# keys = torch_client.create_api_key()
# print(torch_client.get_api_keys())
# torch_client.delete_api_key(keys.accessKey)

# notifications
# print(torch_client.get_notifications())
# print(torch_client.get_incidents())

# analysis pipelines
# print(torch_client.get_analysis_pipeline(1))
# print(torch_client.list_all_analysis_pipelines())

# data sources : create, update, delete
# print(torch_client.get_all_datasources())

# datasource = CreateDataSource(
#     name='snowflake_ds_local',
#     sourceType=SourceType(5, 'SNOWFLAKE'),
#     description='snowflake schema',
#     connectionId=9,
#     configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
#                       ConfigProperty(key='databases.0', value='FINANCE')]
# )
# ds_res = torch_client.create_datasource(datasource)
# ds_res = torch_client.get_datasource('snowflake_ds_local')

# datasource = CreateDataSource(
#     name='snowflake_ds_local',
#     sourceType=SourceType(5, 'SNOWFLAKE'),
#     description='snowflake schema',
#     connectionId=9,
#     configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
#                       ConfigProperty(key='databases.0', value='CRAWLER_DB1')]
# )
# ds_res = ds_res.update_datasource(datasource)

# print(ds_res.get_root_assets())

# auto profile configs
# print(torch_client.get_all_auto_profile_configurations())
# ds_res = torch_client.get_datasource('postgres_ds_local')
# print(ds_res.get_auto_profile_configuration())
# ds_res.remove_auto_profile_configuration()

# asset metadata
# asset = torch_client.get_asset(id=1128)
# metadata = [AssetMetadata('STRING', 'key', 'source', 'value'), AssetMetadata('STRING', 's3_location', 'AWS_S3', 's3://aws/path/test/logs')]
# asset.update_asset_metadata(metadata)
# print(asset.get_asset_metadata())
