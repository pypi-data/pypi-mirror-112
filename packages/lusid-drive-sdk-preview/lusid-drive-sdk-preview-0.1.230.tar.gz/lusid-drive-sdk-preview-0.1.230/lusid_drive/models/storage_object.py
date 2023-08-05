# coding: utf-8

"""
    FINBOURNE Drive API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.1.230
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class StorageObject(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'id': 'str',
        'path': 'str',
        'name': 'str',
        'created_by': 'str',
        'created_on': 'datetime',
        'updated_by': 'str',
        'updated_on': 'datetime',
        'type': 'str',
        'size': 'int',
        'status': 'str',
        'status_detail': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'path': 'path',
        'name': 'name',
        'created_by': 'createdBy',
        'created_on': 'createdOn',
        'updated_by': 'updatedBy',
        'updated_on': 'updatedOn',
        'type': 'type',
        'size': 'size',
        'status': 'status',
        'status_detail': 'statusDetail',
        'links': 'links'
    }

    required_map = {
        'id': 'required',
        'path': 'required',
        'name': 'required',
        'created_by': 'required',
        'created_on': 'required',
        'updated_by': 'required',
        'updated_on': 'required',
        'type': 'required',
        'size': 'optional',
        'status': 'optional',
        'status_detail': 'optional',
        'links': 'optional'
    }

    def __init__(self, id=None, path=None, name=None, created_by=None, created_on=None, updated_by=None, updated_on=None, type=None, size=None, status=None, status_detail=None, links=None):  # noqa: E501
        """
        StorageObject - a model defined in OpenAPI

        :param id:  File or folder identifier (required)
        :type id: str
        :param path:  Path of the folder or file (required)
        :type path: str
        :param name:  Name of the folder or file (required)
        :type name: str
        :param created_by:  Identifier of the user who created the file or folder (required)
        :type created_by: str
        :param created_on:  Date of file/folder creation (required)
        :type created_on: datetime
        :param updated_by:  Identifier of the last user to modify the file or folder (required)
        :type updated_by: str
        :param updated_on:  Date of file/folder modification (required)
        :type updated_on: datetime
        :param type:  Type of storage object (file or folder) (required)
        :type type: str
        :param size:  Size of the file in bytes
        :type size: int
        :param status:  File status corresponding to virus scan status
        :type status: str
        :param status_detail:  Detailed description describing any negative terminal state of file
        :type status_detail: str
        :param links: 
        :type links: list[lusid_drive.Link]

        """  # noqa: E501

        self._id = None
        self._path = None
        self._name = None
        self._created_by = None
        self._created_on = None
        self._updated_by = None
        self._updated_on = None
        self._type = None
        self._size = None
        self._status = None
        self._status_detail = None
        self._links = None
        self.discriminator = None

        self.id = id
        self.path = path
        self.name = name
        self.created_by = created_by
        self.created_on = created_on
        self.updated_by = updated_by
        self.updated_on = updated_on
        self.type = type
        self.size = size
        self.status = status
        self.status_detail = status_detail
        self.links = links

    @property
    def id(self):
        """Gets the id of this StorageObject.  # noqa: E501

        File or folder identifier  # noqa: E501

        :return: The id of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this StorageObject.

        File or folder identifier  # noqa: E501

        :param id: The id of this StorageObject.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if id is not None and len(id) > 40:
            raise ValueError("Invalid value for `id`, length must be less than or equal to `40`")  # noqa: E501
        if id is not None and len(id) < 30:
            raise ValueError("Invalid value for `id`, length must be greater than or equal to `30`")  # noqa: E501
        if (id is not None and not re.search(r'^[a-zA-Z0-9\-]+$', id)):  # noqa: E501
            raise ValueError(r"Invalid value for `id`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-]+$/`")  # noqa: E501

        self._id = id

    @property
    def path(self):
        """Gets the path of this StorageObject.  # noqa: E501

        Path of the folder or file  # noqa: E501

        :return: The path of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this StorageObject.

        Path of the folder or file  # noqa: E501

        :param path: The path of this StorageObject.  # noqa: E501
        :type: str
        """
        if path is None:
            raise ValueError("Invalid value for `path`, must not be `None`")  # noqa: E501
        if path is not None and len(path) > 512:
            raise ValueError("Invalid value for `path`, length must be less than or equal to `512`")  # noqa: E501
        if path is not None and len(path) < 1:
            raise ValueError("Invalid value for `path`, length must be greater than or equal to `1`")  # noqa: E501
        if (path is not None and not re.search(r'^[\/a-zA-Z0-9 \-_]+$', path)):  # noqa: E501
            raise ValueError(r"Invalid value for `path`, must be a follow pattern or equal to `/^[\/a-zA-Z0-9 \-_]+$/`")  # noqa: E501

        self._path = path

    @property
    def name(self):
        """Gets the name of this StorageObject.  # noqa: E501

        Name of the folder or file  # noqa: E501

        :return: The name of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StorageObject.

        Name of the folder or file  # noqa: E501

        :param name: The name of this StorageObject.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if name is not None and len(name) > 50:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `50`")  # noqa: E501
        if name is not None and len(name) < 1:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501
        if (name is not None and not re.search(r'^[A-Za-z0-9_\-\.]+[A-Za-z0-9_\-\. ]*$', name)):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^[A-Za-z0-9_\-\.]+[A-Za-z0-9_\-\. ]*$/`")  # noqa: E501

        self._name = name

    @property
    def created_by(self):
        """Gets the created_by of this StorageObject.  # noqa: E501

        Identifier of the user who created the file or folder  # noqa: E501

        :return: The created_by of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this StorageObject.

        Identifier of the user who created the file or folder  # noqa: E501

        :param created_by: The created_by of this StorageObject.  # noqa: E501
        :type: str
        """
        if created_by is None:
            raise ValueError("Invalid value for `created_by`, must not be `None`")  # noqa: E501

        self._created_by = created_by

    @property
    def created_on(self):
        """Gets the created_on of this StorageObject.  # noqa: E501

        Date of file/folder creation  # noqa: E501

        :return: The created_on of this StorageObject.  # noqa: E501
        :rtype: datetime
        """
        return self._created_on

    @created_on.setter
    def created_on(self, created_on):
        """Sets the created_on of this StorageObject.

        Date of file/folder creation  # noqa: E501

        :param created_on: The created_on of this StorageObject.  # noqa: E501
        :type: datetime
        """
        if created_on is None:
            raise ValueError("Invalid value for `created_on`, must not be `None`")  # noqa: E501

        self._created_on = created_on

    @property
    def updated_by(self):
        """Gets the updated_by of this StorageObject.  # noqa: E501

        Identifier of the last user to modify the file or folder  # noqa: E501

        :return: The updated_by of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this StorageObject.

        Identifier of the last user to modify the file or folder  # noqa: E501

        :param updated_by: The updated_by of this StorageObject.  # noqa: E501
        :type: str
        """
        if updated_by is None:
            raise ValueError("Invalid value for `updated_by`, must not be `None`")  # noqa: E501

        self._updated_by = updated_by

    @property
    def updated_on(self):
        """Gets the updated_on of this StorageObject.  # noqa: E501

        Date of file/folder modification  # noqa: E501

        :return: The updated_on of this StorageObject.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_on

    @updated_on.setter
    def updated_on(self, updated_on):
        """Sets the updated_on of this StorageObject.

        Date of file/folder modification  # noqa: E501

        :param updated_on: The updated_on of this StorageObject.  # noqa: E501
        :type: datetime
        """
        if updated_on is None:
            raise ValueError("Invalid value for `updated_on`, must not be `None`")  # noqa: E501

        self._updated_on = updated_on

    @property
    def type(self):
        """Gets the type of this StorageObject.  # noqa: E501

        Type of storage object (file or folder)  # noqa: E501

        :return: The type of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this StorageObject.

        Type of storage object (file or folder)  # noqa: E501

        :param type: The type of this StorageObject.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def size(self):
        """Gets the size of this StorageObject.  # noqa: E501

        Size of the file in bytes  # noqa: E501

        :return: The size of this StorageObject.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this StorageObject.

        Size of the file in bytes  # noqa: E501

        :param size: The size of this StorageObject.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def status(self):
        """Gets the status of this StorageObject.  # noqa: E501

        File status corresponding to virus scan status  # noqa: E501

        :return: The status of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this StorageObject.

        File status corresponding to virus scan status  # noqa: E501

        :param status: The status of this StorageObject.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def status_detail(self):
        """Gets the status_detail of this StorageObject.  # noqa: E501

        Detailed description describing any negative terminal state of file  # noqa: E501

        :return: The status_detail of this StorageObject.  # noqa: E501
        :rtype: str
        """
        return self._status_detail

    @status_detail.setter
    def status_detail(self, status_detail):
        """Sets the status_detail of this StorageObject.

        Detailed description describing any negative terminal state of file  # noqa: E501

        :param status_detail: The status_detail of this StorageObject.  # noqa: E501
        :type: str
        """

        self._status_detail = status_detail

    @property
    def links(self):
        """Gets the links of this StorageObject.  # noqa: E501


        :return: The links of this StorageObject.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this StorageObject.


        :param links: The links of this StorageObject.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, StorageObject):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
