#!/bin/bash
egrep -r "overallHits::total|overallMisses::total|board.memory.mem_ctrl.dram.avgMemAccLat|board.memory.mem_ctrl.dram.numReads::total|board.memory.mem_ctrl.dram.numWrites::total" $1
egrep -r "overallMissLatency::total" $1
egrep -r "board.memory.mem_ctrl.dram.totQLat|board.memory.mem_ctrl.dram.totBusLat|board.memory.mem_ctrl.dram.totMemAccLat" $1
