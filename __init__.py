import grpc
import time

from locust import Locust, events


class GrpcClient(object):
    def __init__(self, stub_cls, channel, timeout):
        self.stub = stub_cls(grpc.insecure_channel(channel))
        self.timeout = timeout

    def __getattr__(self, name):
        def wrapper(argument):
            func = getattr(self.stub, name)
            start_time = time.time()

            result = None
            try:
                result = func(argument, timeout=self.timeout)
            except BaseException as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(
                    request_type="grpc", name=name,
                    response_time=total_time, exception=e
                )
            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(
                    request_type="grpc", name=name,
                    response_time=total_time, response_length=result.ByteSize()
                )
            return result
        return wrapper


class GrpcLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(GrpcLocust, self).__init__(*args, **kwargs)
        self.client = GrpcClient(self.stub_cls, self.channel, self.timeout)
