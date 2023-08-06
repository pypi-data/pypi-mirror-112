

class _DataObject:
    """Base class for Metadata and Exifdata.

    TODO: Implement more common utilities here (e.g. is_serializable) 

    """

    def to_dict(self):
        """Returns all attributes of an object as a dictionary.

        """
        return vars(self)
