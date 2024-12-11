from gem5.components.cachehierarchies.classic.no_cache import NoCache

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
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
    cache_hierarchy=NoCache(),
    memory=SingleChannelDDR3_1600(size="1GB"),
    clk_freq="1GHz",
    processor=processor,
)

binary_path = Path("/home/ubuntu/123/arr_sort_random_4mb_x4")
board.set_se_binary_workload(
    binary = BinaryResource(
        local_path=binary_path.as_posix()
    )
)
sim = Simulator(board)

sim.run()
