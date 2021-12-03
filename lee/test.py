#
# This file is part of LiteX.
#
# Copyright (c) 2020-2021 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.misc import WaitTimer

from litex.soc.interconnect.csr import *

class LeeTest(Module, AutoCSR):
    def __init__(self, pads, sys_clk_freq, period=3e0):
        self.pads = pads
        self._out = CSRStorage(len(pads), description="Lee output")

        n = len(pads)
        timer = WaitTimer(int(period*sys_clk_freq))
        self.submodules += timer

        #
        # If the timer is running then the LEDs are set to the CSR value
        # and if it's finished then 0
        #
        self.comb += [
                If(timer.wait,
                    pads.eq(self._out.storage)
                ).Else(
                    pads.eq(0)
                ) 
            ]

        #
        # If we write to the register then we need to start the timer
        #
        self.sync += If(self._out.re, timer.wait.eq(1))

        #
        # If the timer is done then turn off wait
        #
        self.sync += If(timer.done, timer.wait.eq(0))
                    


## # Led Chaser ---------------------------------------------------------------------------------------
## 
## _CHASER_MODE  = 0
## _CONTROL_MODE = 1
## 
## class XLedChaser(Module, AutoCSR):
##     def __init__(self, pads, sys_clk_freq, period=1e0):
##         self.pads = pads
##         self._out = CSRStorage(len(pads), description="Led Output(s) Control.")
## 
##         # # #
## 
##         n      = len(pads)
##         chaser = Signal(n)
##         mode   = Signal(reset=_CHASER_MODE)
##         timer  = WaitTimer(int(period*sys_clk_freq/(2*n)))
##         self.submodules += timer
##         self.comb += timer.wait.eq(~timer.done)
##         self.sync += If(timer.done, chaser.eq(Cat(~chaser[-1], chaser)))
##         self.sync += If(self._out.re, mode.eq(_CONTROL_MODE))
##         self.comb += [
##             If(mode == _CONTROL_MODE,
##                 pads.eq(self._out.storage)
##             ).Else(
##                 pads.eq(chaser)
##             )
##         ]
## 
