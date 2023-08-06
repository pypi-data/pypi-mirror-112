# Group


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**members** | [**[GroupMember]**](GroupMember.md) | List of members in the group | [optional] 
**member_of** | [**[UserIdentity]**](UserIdentity.md) | List of groups that the user is a member of | [optional] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**external_id** | **str, none_type** | External unique identifier | [optional] 
**enabled** | **bool** | Enable/Disable a user | [optional] 
**status** | [**UserStatusEnum**](UserStatusEnum.md) |  | [optional] 
**first_name** | **str** | User&#39;s first name | [optional] 
**last_name** | **str** | User&#39;s last name | [optional] 
**email** | [**Email**](Email.md) |  | [optional] 
**provider** | **str, none_type** | Upstream IdP name | [optional] 
**roles** | [**Roles**](Roles.md) |  | [optional] 
**org_id** | **str** | Unique identifier | [optional] 
**type** | **str** | Type of user | [optional] [readonly] 
**created** | **datetime** | Creation time | [optional] [readonly] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**auto_created** | **bool** | Whether the user was automatically created as part of another process such as logging in. On creation, this flag being true serves to trigger any behaviour tied to automatically created users, such as addition to special groups. On read, it can serve to indicate whether the user was automatically created. On update it will ensure that the automatically triggered behaviour still holds true.  | [optional]  if omitted the server will use the default value of False
**upstream_user_identities** | [**[UpstreamUserIdentity]**](UpstreamUserIdentity.md) | The upstream identities this user can use to log in to the system. When a user logs in, their identity in this system will be determined by matching against this list. Note that this implies that entries in this list are globally unique.  | [optional] [readonly] 
**cascade** | **bool** | Whether the user will be added to sub organisations automatically. When set for a user that is a member of a particular organisation, subsequent creations of sub organisations will add this user to that suborgansation.  | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


