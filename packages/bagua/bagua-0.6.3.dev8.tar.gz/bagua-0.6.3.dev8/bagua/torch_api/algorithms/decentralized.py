#!/usr/bin/env python3

from bagua.torch_api.bucket import BaguaBucket
from bagua.torch_api.tensor import BaguaTensor
from bagua.torch_api.distributed import BaguaModule
from bagua.torch_api.algorithms import Algorithm
from typing import List
import torch


class DecentralizedAlgorithm(Algorithm):
    def __init__(
        self,
        peer_selection_mode: str = "all",
        compression: str = None,
        communication_interval: int = 1,
    ):
        """
        Create an instance of the
        `Decentralized <https://baguasys.github.io/tutorials/algorithms/decentralized.html>`_
        algorithm.

        Args:
            peer_selection_mode (str): Can be "all" or "shift_one". "all" means all workers'
                weights are averaged in each communication step. "shift_one" means each worker
                selects a different peer to do weights average in each communication step.
            compression (str): Not supported yet.
            communication_interval (int): Number of iterations between two communication steps.
        """
        self.peer_selection_mode = peer_selection_mode
        self.compression = compression
        self.communication_interval = communication_interval
        self.tensor_groups = []

    def init_tensors(self, bagua_module: BaguaModule) -> List[BaguaTensor]:
        parameters = bagua_module.bagua_build_params()
        self.tensors = [
            param.ensure_bagua_tensor(name) for name, param in parameters.__reversed__()
        ]
        return self.tensors

    def init_forward_pre_hook(self, bagua_module: BaguaModule):
        def hook(input):
            for tensor in self.tensors:
                tensor.bagua_mark_communication_ready()

        return hook

    def init_backward_hook(self, bagua_module: BaguaModule):
        def hook(parameter_name, parameter):
            return

        return hook

    def init_post_backward_hook(self, bagua_module: BaguaModule):
        def hook():
            bagua_module._bagua_backend.wait_pending_comm_ops()
            torch.cuda.synchronize()
            bagua_module._bagua_backend.execute_post_backward_comm_ops()
            bagua_module._bagua_backend.wait_pending_post_backward_comm_ops()

        return hook

    def init_operations(
        self,
        bagua_module: BaguaModule,
        bucket: BaguaBucket,
    ):
        bucket.clear_ops()
        bucket.append_decentralized_synchronous_op(
            hierarchical=True,
            peer_selection_mode=self.peer_selection_mode,
            communication_interval=self.communication_interval,
        )
