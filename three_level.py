from gem5.components.boards.abstract_board import AbstractBoard
from gem5.components.cachehierarchies.classic.abstract_classic_cache_hierarchy import (
    AbstractClassicCacheHierarchy,
)

from gem5.components.cachehierarchies.classic.caches.l1dcache import L1DCache
from gem5.components.cachehierarchies.classic.caches.l1icache import L1ICache
from gem5.components.cachehierarchies.classic.caches.l2cache import L2Cache
from gem5.components.cachehierarchies.classic.caches.mmu_cache import MMUCache

from gem5.isas import ISA

from m5.objects import (
    BadAddr,
    Cache,
    L2XBar,
    SystemXBar,
    SubSystem,
)
from m5.params import Port
from m5.objects import Cache, LRURP, FIFORP, DuelingRP, SHiPMemRP



class PrivateL1PrivateL2SharedL3CacheHierarchy(AbstractClassicCacheHierarchy):

    def __init__(
        self,
        l1d_size,
        l1i_size,
        l2_size,
        l3_size,
        l1d_assoc,
        l1i_assoc,
        l2_assoc,
        l3_assoc,
    ):
        AbstractClassicCacheHierarchy.__init__(self)

        # Save the sizes to use later. We have to use leading underscores
        # because the SimObject (SubSystem) does not have these attributes as
        # parameters.
        self._l1d_size = l1d_size
        self._l1i_size = l1i_size
        self._l2_size = l2_size
        self._l3_size = l3_size
        self._l1d_assoc = l1d_assoc
        self._l1i_assoc = l1i_assoc
        self._l2_assoc = l2_assoc
        self._l3_assoc = l3_assoc

        ## FILL THIS IN
        self.membus = SystemXBar(width=64)

        # For FS mode
        self.membus.badaddr_responder = BadAddr()
        self.membus.default = self.membus.badaddr_responder.pio

    ## FILL THIS IN
    def get_mem_side_port(self) -> Port:
        return self.membus.mem_side_ports

    def get_cpu_side_port(self) -> Port:
        return self.membus.cpu_side_ports

    def incorporate_cache(self, board: AbstractBoard):
        """
        Here, we create the caches and connect them together
        """
        board.connect_system_port(self.membus.cpu_side_ports)

        # connect the caches to memory
        for _, port in board.get_memory().get_mem_ports():
            self.membus.mem_side_ports = port

        self.l3_bus = L2XBar()

        self.clusters = [
            self._create_core_cluster(
                core, self.l3_bus, board.get_processor().get_isa()
            )
            for core in board.get_processor().get_cores()
        ]

        self.l3_cache = L3Cache(size=self._l3_size, assoc=self._l3_assoc)
        self.l3_cache.mem_side = self.membus.cpu_side_ports
        self.l3_cache.cpu_side = self.l3_bus.mem_side_ports

        if board.has_coherent_io():
            self._setup_io_cache(board)

    def _create_core_cluster(self, core, l3_bus, isa):
        """
        Create a core cluster with the given core.
        """
        cluster = SubSystem()

        ## FILL THIS IN
        # Create the L1 and L2 caches, l2xbar, and connect them to the core
        cluster.l1d_cache = L1DCache(
            size=self._l1d_size, assoc=self._l1d_assoc
        )
        cluster.l1i_cache = L1ICache(
            size=self._l1i_size, assoc=self._l1i_assoc
        )

        core.connect_icache(cluster.l1i_cache.cpu_side)
        core.connect_dcache(cluster.l1d_cache.cpu_side)

        cluster.l2_cache = L2Cache(
                size=self._l2_size, 
                assoc=self._l2_assoc,
                tag_latency = 3,
                data_latency = 3
                )
        cluster.l2_bus = L2XBar()

        cluster.l1d_cache.mem_side = cluster.l2_bus.cpu_side_ports
        cluster.l1i_cache.mem_side = cluster.l2_bus.cpu_side_ports
        cluster.l2_cache.cpu_side = cluster.l2_bus.mem_side_ports

        cluster.l2_cache.mem_side = l3_bus.cpu_side_ports

        cluster.iptw_cache = MMUCache(size="8KiB", writeback_clean=False)
        cluster.dptw_cache = MMUCache(size="8KiB", writeback_clean=False)
        core.connect_walker_ports(
            cluster.iptw_cache.cpu_side, cluster.dptw_cache.cpu_side
        )

        # Connect the caches to the L2 bus
        cluster.iptw_cache.mem_side = cluster.l2_bus.cpu_side_ports
        cluster.dptw_cache.mem_side = cluster.l2_bus.cpu_side_ports

        if isa == ISA.X86:
            int_req_port = self.membus.mem_side_ports
            int_resp_port = self.membus.cpu_side_ports
            core.connect_interrupt(int_req_port, int_resp_port)
        else:
            core.connect_interrupt()

        return cluster

    def _setup_io_cache(self, board: AbstractBoard) -> None:
        """Create a cache for coherent I/O connections"""
        self.iocache = Cache(
            assoc=8,
            tag_latency=5,
            data_latency=5,
            response_latency=5,
            mshrs=20,
            size="1kB",
            tgts_per_mshr=12,
            addr_ranges=board.mem_ranges,
        )
        self.iocache.mem_side = self.membus.cpu_side_ports
        self.iocache.cpu_side = board.get_mem_side_coherent_io_port()


class L3Cache(Cache):
    """
    This class represents an L3 cache.
    """

    def __init__(self, size: str, assoc: int):
        super().__init__()

        self.size = size
        self.assoc = assoc
        self.tag_latency = 6
        self.data_latency = 6
        self.response_latency = 6
        self.mshrs = 20
        self.tgts_per_mshr = 12
        self.writeback_clean = False
        self.clusivity = "mostly_incl"
        self.replacement_policy = LRURP()
#        self.replacement_policy = SHiPMemRP()
#        self.replacement_policy = FIFORP()
