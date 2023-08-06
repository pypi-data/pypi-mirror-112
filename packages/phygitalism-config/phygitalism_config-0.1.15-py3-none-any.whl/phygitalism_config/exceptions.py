class MissingException(Exception):
    def __init__(self, klass_name, name):
        super(MissingException, self).__init__("{} missing {}".format(klass_name, name))
