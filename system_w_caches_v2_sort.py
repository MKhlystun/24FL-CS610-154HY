from three_level import PrivateL1PrivateL2SharedL3CacheHierarchy

from gem5.components.boards.test_board import TestBoard
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.memory.single_channel import SingleChannelDDR3_2133
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.components.processors.gups_generator import GUPSGenerator
from gem5.resources.resource import BinaryResource
from gem5.isas import ISA
from pathlib import Path
import m5.debug


from gem5.simulate.simulator import Simulator

processor = SimpleProcessor(
    cpu_type = CPUTypes.TIMING,
    num_cores = 1,
    isa = ISA.X86
)
board = SimpleBoard(
    cache_hierarchy=PrivateL1PrivateL2SharedL3CacheHierarchy(
        l1d_size="4KiB",
        l1d_assoc=4,
        l1i_size="4KiB",
        l1i_assoc=4,
        l2_size="32KiB",
        l2_assoc=4,
        l3_size="1MiB",
        l3_assoc=8,
    ),
    memory=SingleChannelDDR3_1600(size="1GB"),
    clk_freq="1GHz",
    processor=processor,
)

binary_path = Path("/home/ubuntu/123/arr_sort_05mb")
board.set_se_binary_workload(
    binary = BinaryResource(
        local_path=binary_path.as_posix()
    )
)
sim = Simulator(board)

sim.run()
