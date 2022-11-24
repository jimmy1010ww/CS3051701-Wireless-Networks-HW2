import socket
import os

# Serve Info
HOST = '127.0.0.1'
PORT = 12000
calc_mode = 0

#File IO
ANS_FILE_NAME = 'ans.txt'
INPUT_FILE_NAME = 'Testcase.txt'

#初始化客戶端的 socket
def initClientSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

#取得計算機的模式 1:手動輸入 2:檔案輸入 q:離開
def getCalcMode():
    while True:
        print("Please input the calculation mode:")
        print("1 -> Manual input")
        print("2 -> Read from file")
        print("q -> Quit")

        user_input = input('$')
        if user_input == '1':
            return '1'
        elif user_input == '2':
            return '2'
        elif user_input == 'q' or 'Q':
            return 'q'
        else:
            print("Invalid input")


if __name__ == "__main__":
    os.system("clear")

    client_socket = initClientSocket()

    while True:
        send_mode = getCalcMode()
        print('Choose mode => ' + send_mode)

        if send_mode == 'q' or send_mode == 'Q':
            client_socket.send("q".encode("utf-8"))
            print("Bye~")
            quit()
        else:
            client_socket.send(send_mode.encode("utf-8"))
            calc_mode = int(send_mode)
    
        indata = client_socket.recv(1024)
        if len(indata) == 0: # connection closed
            client_socket.close()
            print('server closed connection.')
            break
        elif indata == 'OK':
            print('Server ready to receive data.')


        
        if calc_mode == 1:
            while True:
                print("Please input the calculation expression, or input 'q' to quit.")
                user_input = input('$')
                if user_input == 'q' or user_input == 'Q':
                    client_socket.send("MODE_QUIT".encode("utf-8"))
                    calc_mode = 0
                    break
                else:
                    client_socket.send(user_input.encode("utf-8"))
                    indata = client_socket.recv(1024)
                    print('ANS => ' + indata.decode("utf-8"))
        elif calc_mode == 2:
            with open(os.getcwd() + '/' + INPUT_FILE_NAME,'rb') as f:
                l = f.read(1024)
                while (l):
                    print ('Sending...')
                    client_socket.send(l)
                    l = f.read(1024)
                f.close()

            print('send done.')




