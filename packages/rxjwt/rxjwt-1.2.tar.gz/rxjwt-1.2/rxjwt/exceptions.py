class InvalidAlgorithmException(Exception):
    """
    An exception of invalid hashing algorithm
    """

    def __init__(self, algorithm, algorithms):
        """
        A constructor with just sets the algorithm property (the wrong algorithm
        name).
        :param algorithm: The wrong algorithm name.
        :param algorithms: All available algorithms.
        """
        self.algorithm = algorithm
        self.algorithms = algorithms

    def __str__(self):
        """
        Returns the exception message.
        :return: An exception message which contains info about possible
        algorithms.
        """
        return "Wrong algorithm: {algorithm}. The algorithm must be one of the" \
               "following: {algorithms}".format(algorithm=self.algorithm,
                                                algorithms=",".join(self.algorithms.keys()))


class IncorrectTokenHeaderException(Exception):
    pass


class IncorrectTokenPayloadException(Exception):
    pass
