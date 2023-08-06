#Datasource APIs

Torch SDK has full access on catalog APIs as well. Using torch sdk, one can create datasource and version it with associated assets, relations.
##### Create Datasource
Torch sdk has access to create or update existing datasource. Torch has support for virtual datasource as well for ML purpose and some non-virtual/real as well for example relational databases, file based databases et cetera. To create datasource, source type details are required. To get all source types supported in torch, use `get_all_source_types()` method.
```python
from torch_sdk.models.datasource import CreateDataSource, SourceType

datasource = CreateDataSource(
    name='Feature_bag_datasource_sdk',
    sourceType=SourceType(21, 'FEATURE_BAG'),
    description='feature bag assembly creation using python sdk',
    isVirtual=True
)
datasource_response = torch_client.create_datasource(datasource)
```

##### Create New Version Of Datasource
Torch sdk can version the datasource as well. Torch sdk can initiate new version the datasource and return latest instance of it. It has also method to get current latest snapshot version.
```python
# get data source
datasource_response = torch_client.get_datasource('Feature_bag_datasource')

# create new version of the datasource
new_snapshot_version = datasource_response.initialise_snapshot(uid='Habcfc38-9daa-4842-b008-f7fb3dd8439a')

# get current snapshot data
current_snapshot_version = datasource_response.get_current_snapshot()
```
##### Create Asset And Relations B/w Them
You can create/update assets and relations between them.
With use of the torch sdk, user can create assets in datasource and can also define relations between assets. To get asset types supported in torch, use `get_asset_types()` method. Torch sdk has methods to get existing relations and assets in the given datasource.
```python
from torch_sdk.models.create_asset import AssetMetadata

# get asset by id/uid
datasource_response = torch_client.get_datasource('Feature_bag_datasource')

# create assets
asset_1 = datasource_response.create_asset(uid='Feature_bag_datasource.feature_1',
                                            metadata=[AssetMetadata('STRING', 'abcd', 'pqr', 'sds')],
                                            asset_type_id=22,
                                            description='feature 1 asset.',
                                            name='car feature'
                                                )
asset_2 = datasource_response.create_asset(uid='Feature_bag_datasource.feature_2',
                                            metadata=[AssetMetadata('STRING', 'abcd', 'pqr', 'sds')],
                                            asset_type_id=22,
                                            description='feature asset 2',
                                            name='bike feature'
                                                )

# create asset relation
toAssetUUID = 'postgres-assembly-5450.ad_catalog.ad_catalog.qrtz_simple_triggers'
relationType = RelationType.SIBLING
asset_relation_1_to_2 = asset_1.create_asset_relation(relation_type=relationType, to_asset_uuid=toAssetUUID)

# get asset by id/uid
asset = datasource_response.get_asset(id=1)
asset = datasource_response.get_asset(uid='Feature_bag_datasource.feature_1')

```