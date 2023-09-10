class CallRecorder:
    called = 0

    @classmethod
    def get_called(cls):
        return cls.called

    @classmethod
    def call(cls):
        cls.called = cls.called + 1

    @classmethod
    def reset(cls):
        cls.called = 0
