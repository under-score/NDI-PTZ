#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Tue Dec 31 17:35:18 2024
Moves PTZ NDI video camera
Runs on Mac under Sequoia 15.1
Needs Python 3.8
Needs NDI SDK https://ndi.video/for-developers/ndi-sdk/download/
Needs the libraries signal, time and NDIlib
Based on example code at NDI SDK (NDIlib_Recv_PTZ.cpp)
Includes an intentional typo ndi.FRANE_TYPE_STATUS_CHANGE instead of ndi.FRAME_TYPE_STATUS_CHANGE
With help of ChatGPT o1

@author: wjst
"""

import signal
import time
import NDIlib as ndi

# Global flag for exit control
exit_loop = False

def sigint_handler(signum, frame):
    global exit_loop
    exit_loop = True

def main():
    # Initialize NDI
    if not ndi.initialize():
        print("Cannot run NDI.")
        return 0

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, sigint_handler)

    # Create NDI finder
    ndi_find = ndi.find_create_v2()
    if ndi_find is None:
        return 0

    # Wait for sources
    sources = []
    while not exit_loop and not sources:
        print('Looking for sources ...')
        ndi.find_wait_for_sources(ndi_find, 1000)
        sources = ndi.find_get_current_sources(ndi_find)

    # Check if we have any sources
    if not sources:
        return 0

    # Create receiver
    recv_create_desc = ndi.RecvCreateV3()
    recv_create_desc.source_to_connect_to = sources[0]
    recv_create_desc.ndi_recv_name = "Example PTZ Receiver"

    ndi_recv = ndi.recv_create_v3(recv_create_desc)
    if ndi_recv is None:
        return 0

    # Destroy the finder since we don't need it anymore
    ndi.find_destroy(ndi_find)

    # Run for 30 seconds
    start_time = time.time()
    while not exit_loop and (time.time() - start_time) < 30:
        # Receive frames
        frame_type, _, _, _ = ndi.recv_capture_v2(ndi_recv, 1000)

        # Handle status changes
        if frame_type == ndi.FRANE_TYPE_STATUS_CHANGE:
            # Check if PTZ is supported
            if ndi.recv_ptz_is_supported(ndi_recv):
                print("This source supports PTZ functionality. Moving to preset #3.")
                # Move to preset 3 at full speed
                ndi.recv_ptz_recall_preset(ndi_recv, 3, 1.0)

    # Clean up
    ndi.recv_destroy(ndi_recv)
    ndi.destroy()

    return 0

if __name__ == "__main__":
    exit(main())
