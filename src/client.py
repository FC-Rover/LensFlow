#!/usr/bin/env python3

import cv2
import numpy as np
import socket
import struct
import pickle


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


hostip = socket.gethostbyname(hostname)

server_address = 'hostip'  
server_port = 10051
client_socket.connect((server_address, server_port))
def main():
    
    #data from the server
    data = b""
    payload_size = struct.calcsize(">L")

    try:
        while True:
            #message size
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            
        
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            #feserialise frame data
            frame = pickle.loads(frame_data)

            
            #resulting frame
            cv2.imshow('Video Stream', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        #release  capture
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()