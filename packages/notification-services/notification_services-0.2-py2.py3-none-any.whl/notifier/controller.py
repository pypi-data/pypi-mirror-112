from abc import ABCMeta, abstractmethod

class NotificationController(metaclass=ABCMeta):

    @abstractmethod
    def _send_notification(self, data: dict):
        pass

    @abstractmethod
    def _process_data(self, **data):
        pass

    def notify(self, **data):
        self._process_data(**data)
        rsp = self._send_notification()
        return rsp


from providers import _all_providers

def all_providers() -> list:
    return list(_all_providers.keys())

def get_notifier(provider_name: str) -> NotificationController:

    if provider_name in _all_providers:
        return _all_providers[provider_name]()
    # Add exception


def notify(provider_name: str, **data):
    # get_notifier(provider_name)
    return get_notifier(provider_name).notify(**data)
