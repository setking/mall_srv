import abc


class Register(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def register(self, name, id, address, port, tags):
        pass

    @abc.abstractmethod
    def register_grpc(self, name, id, address, port, tags):
        pass

    @abc.abstractmethod
    def unregister(self, service_id):
        pass

    @abc.abstractmethod
    def get_all_services(self):
        pass

    @abc.abstractmethod
    def filter_service(self, service):
        pass
