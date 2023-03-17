import warnings

import bson
from marshmallow import fields
from marshmallow.exceptions import ValidationError
from marshmallow.utils import (_Missing, callable_or_raise, is_collection,
                               isoformat)

missing_ = _Missing()


class ObjectId(fields.Field):

    def _serialize(self, value, attr, obj):
        """
        To JSON\Dict, whatever primitive
        :param value:
        :param attr:
        :param obj:
        :return:
        """
        if value is None:
            return None
        return str(value)

    def _deserialize(self, value, attr, data):
        """
        To object -> to ObjectId
        :param value:
        :param attr:
        :param data:
        :return:
        """
        # print('serialize ObjId')
        if not bson.objectid.ObjectId.is_valid(value):
            self.fail('invalid')
        return bson.ObjectId(value)


class Method(fields.Field):
    """A field that takes the value returned by a `Schema` method.

    :param str method_name: The name of the Schema method from which
        to retrieve the value. The method must take an argument ``obj``
        (in addition to self) that is the object to be serialized.
    :param str deserialize: Optional name of the Schema method for deserializing
        a value The method must take a single argument ``value``, which is the
        value to deserialize.

    .. versionchanged:: 2.0.0
        Removed optional ``context`` parameter on methods. Use ``self.context`` instead.
    .. versionchanged:: 2.3.0
        Deprecated ``method_name`` parameter in favor of ``serialize`` and allow
        ``serialize`` to not be passed at all.
    """
    _CHECK_ATTRIBUTE = False

    def __init__(self, serialize=None, deserialize=None, method_name=None, **kwargs):
        if method_name is not None:
            warnings.warn('"method_name" argument of fields.Method is deprecated. '
                          'Use the "serialize" argument instead.', DeprecationWarning)

        self.serialize_method_name = self.method_name = serialize or method_name
        self.deserialize_method_name = deserialize
        super(Method, self).__init__(**kwargs)

    def _serialize(self, value, attr, obj):
        if not self.serialize_method_name:
            return missing_

        method = callable_or_raise(
            getattr(self.parent, self.serialize_method_name, None)
        )
        try:
            return method(obj, **self.metadata)  # <- Passing metadata into serialization function
        except AttributeError:
            pass
        return missing_

    def _deserialize(self, value, attr, data):
        if self.deserialize_method_name:
            try:
                method = callable_or_raise(
                    getattr(self.parent, self.deserialize_method_name, None)
                )
                return method(value, **self.metadata)  # <- Passing metadata into deserialization function
            except AttributeError:
                pass
        return value


class DateTimeISO(fields.DateTime):
    """

    """

    def __init__(self, timespec='milliseconds', **kwargs):
        super().__init__(format=None, **kwargs)
        self.timespec = timespec

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            return isoformat(value, localtime=self.localtime, timespec=self.timespec)
        except (AttributeError, ValueError) as err:
            self.fail('format', input=value)

    # TODO: add deserialization
