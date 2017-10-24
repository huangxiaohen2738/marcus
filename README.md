# Test



from manifest_proto.manifest_pb2_grpc import ManifestServiceStub
from manifest_proto.manifest_pb2 import GetSkuListBySpu

from marcus import GrpcLocust

class ManifestTest(GrpcLocust):
    stub_cls = ManifestServiceStub
    channel = "localhost:50002"
    timeout = 1000

    min_wait = 100
    max_wait = 200

    class task_set(TaskSet):
        def get_spu_id():
            return str(random.randint(50, 100))

        @task(10)
        def list(self):
            req = GetSkuListRequest(store_id="12345", spu_id=self.get_spu_id())
            res = self.client.GetSkuListBySpu(req)
