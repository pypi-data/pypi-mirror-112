"""TPURunner class."""
import asyncio
from typing import Dict
import numpy as np

from iva_tpu import TPUDevice, TPUProgram, TPUProgramInfo, TPUInference
from .runner import Runner


class TPURunner(Runner):
    """Runner for IVA TPU."""

    def __init__(self, program_path: str, loop=None, sync=False):
        """
        Program initialization.

        Parameters
        ----------
        program_path
            path to TPU program
        """
        self.program = TPUProgram(program_path, TPUProgramInfo())
        input_nodes = self.get_input_nodes()
        output_nodes = self.get_output_nodes()
        self.sync = sync

        self.loop = loop if loop else asyncio.get_event_loop()

        super().__init__(program_path, input_nodes, output_nodes)

        self.device = TPUDevice()
        self.device.load_program(self.program)

    def __call__(self, tensors: Dict[str, np.ndarray], dtype=np.float32) -> Dict[str, np.ndarray]:
        """
        Run inference using IVA TPU.

        Parameters
        ----------
        tensors
            Input tensors for inference
        dtype
            The desired data-type for the returned data (np.float32 or np.int8)
            If not given, then the type will be determined as np.float32.

        Returns: Result after TPU
        -------

        """
        inference = TPUInference(self.program)
        inference.load_tensors_dict(tensors)

        if self.sync:
            self.device.load_inference_sync(inference)
        else:
            status_future = self.device.load_inference(inference)
            self.loop.run_until_complete(status_future)

        tpu_out_tensors = inference.get_tensors_dict()
        return tpu_out_tensors

    def get_input_nodes(self) -> list:
        """
        Get a list of names of the graph input nodes.

        Returns
        -------
        A list of names of input nodes
        """
        input_nodes = [n[1]["anchor"] for d in self.program.metadata['inputs'].values() for n in d]
        return input_nodes

    def get_output_nodes(self) -> list:
        """
        Get a list of names of the graph output nodes.

        Returns
        -------
        A list of names of output nodes
        """
        output_nodes = [n[1]["anchor"] for d in self.program.metadata['outputs'].values() for n in d]
        return output_nodes
