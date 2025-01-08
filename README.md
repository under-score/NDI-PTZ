# NDI-PTZ

A proof of principle python script that moves a NDI video camera in PTZ directions

Needs MacOS, tested under Sequoia 15.1

Needs Python 3.8

Needs NDI SDK https://ndi.video/for-developers/ndi-sdk/download
NDI is a registered trademark of Vizrt NDI AB 

Needs the libraries signal, time and NDIlib

Firewall is OK but disable any VPN

Based on example code of NDI SDK NDIlib_Recv_PTZ.cpp and https://github.com/buresu/ndi-python

Includes an intentional typo ndi.FRANE_TYPE_STATUS_CHANGE instead of ndi.FRAME_TYPE_STATUS_CHANGE

With help of ChatGPT o1
