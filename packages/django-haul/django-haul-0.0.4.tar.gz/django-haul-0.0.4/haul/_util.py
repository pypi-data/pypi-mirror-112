class UncloseableStream:
    def __init__(self, stream):
        self._stream = stream

    # Prevents ZipFile from closing the stream
    def __getattribute__(self, name: str):
        if name == 'close':
            return lambda: None
        return getattr(object.__getattribute__(self, '_stream'), name)
