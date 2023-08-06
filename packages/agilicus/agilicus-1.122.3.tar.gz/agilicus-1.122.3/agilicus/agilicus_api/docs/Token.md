# Token

Object describing the properties of a token

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub** | **str** | Unique identifier | [optional] [readonly] 
**sub_email** | [**Email**](Email.md) |  | [optional] 
**org** | **str** | Unique identifier | [optional] [readonly] 
**root_org** | **str** | The organisation at the root of the hierachy for which this token provides permissions.  | [optional] [readonly] 
**roles** | [**Roles**](Roles.md) |  | [optional] 
**jti** | **str** | Unique identifier | [optional] [readonly] 
**iat** | **str** | token issue date | [optional] [readonly] 
**exp** | **str** | token expiry date | [optional] [readonly] 
**hosts** | [**[HostPermissions]**](HostPermissions.md) | array of valid hosts | [optional] 
**aud** | **[str]** | token audience | [optional] [readonly] 
**session** | **str** | Unique identifier | [optional] [readonly] 
**scopes** | [**[TokenScope]**](TokenScope.md) | The list of scopes associated with this access token. Note that these scopes do not indicate whether that permission has been granted. Whether or not the permission has been granted to this token depends on the scope being associated with the token AND whether the user has that permission to begin with.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


