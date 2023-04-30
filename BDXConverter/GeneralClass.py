from io import BytesIO


class GeneralClass:
    """
    Any operation of the BDX file will inherit this class
    """

    def __init__(self) -> None:
        self.operationNumber: int
        self.operationName: str

    def Marshal(self, writer: BytesIO) -> None:
        """
        Marshal python object which named GeneralClass into the writer
        """
        ...

    def UnMarshal(self, buffer: BytesIO) -> None:
        """
        Unmarshal buffer(io object) into the python object which named GeneralClass
        """
        ...

    def Loads(self, jsonDict: dict) -> None:
        """
        Convert jsonDict:dict into python object which named GeneralClass
        """
        ...

    def Dumps(self) -> dict:
        """
        Convert python object which named GeneralClass into dictionary
        """
        return self.__dict__
