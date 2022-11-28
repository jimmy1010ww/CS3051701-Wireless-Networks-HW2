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

        user_input = input('$ ')
        if user_input == '1':
            return '1'
        elif user_input == '2':
            return '2'
        elif user_input == 'q' or 'Q':
            return 'q'
        else:
            print("Invalid input")

def fileRecv(fileName, socket):
    #打開要接收文件
    with open(os.getcwd() + '/' + fileName,'wb') as f:
        #開始接收文件
        while True:
            print ("Receiving...")
            data = socket.recv(1024)
            f.write(data)
            #如果檔案長度不夠1024則表示接收完畢
            if len(data) < 1024:
                break
        #檔案關閉
        f.close()
    print('receive done')

def fileSend(fileName, socket):
    #打開要傳送的文件
    with open(os.getcwd() + '/' + fileName,'rb') as f:
        #開始傳送文件
        l = f.read(1024)
        #如果檔案長度不夠1024則表示傳送完畢
        while (l):
            print ('Sending...')
            socket.send(l)
            l = f.read(1024)
        #檔案關閉
        f.close()
    print('send done.')

if __name__ == "__main__":
    os.system("clear")

    #獲取與伺服器的socket
    client_socket = initClientSocket()

    try:
        while True:
            #取得計算機的模式
            send_mode = getCalcMode()
            print('Choose mode => ' + send_mode)

            #如果選擇離開則離開
            if send_mode == 'q' or send_mode == 'Q':
                client_socket.send("q".encode("utf-8"))
                print("Bye~")
                quit()
            else:
                client_socket.send(send_mode.encode("utf-8"))
                calc_mode = int(send_mode)
        
            #接收伺服器回應
            indata = client_socket.recv(1024)

            #連線關閉
            if len(indata) == 0:
                client_socket.close()
                print('server closed connection.')
                break
            #伺服器回應 OK
            elif indata == 'OK':
                print('Server ready to receive data.')


            #根據計算機模式執行
            if calc_mode == 1:  #單行執行
                while True:
                    print("Please input the calculation expression, or input 'q' to quit.")
                    user_input = input('$ ')

                    #如果輸入q回到選擇模式（預設)
                    if user_input == 'q' or user_input == 'Q':
                        client_socket.send("MODE_QUIT".encode("utf-8"))
                        calc_mode = 0
                        break
                    else:
                        #傳送輸入的計算式到伺服器端
                        client_socket.send(user_input.encode("utf-8"))
                        #接收伺服器端的回應
                        indata = client_socket.recv(1024)
                        indata = indata.decode("utf-8")

                        #如果伺服器回應為 'Invalid input' 則重新輸入
                        if indata == "Invalid input":
                            print('Invalid input')
                            continue
                        else:
                        #反之輸出伺服器端的回應
                            print('ANS => {:.2f}'.format(float(indata)))
            #檔案傳輸模式
            elif calc_mode == 2:
                #傳送 Testcase.txt
                fileSend(INPUT_FILE_NAME, client_socket)

                #等待伺服器回傳 ans.txt，超過 10 秒則離開
                client_socket.settimeout(10)
                try:
                    #接收伺服器回應的訊號
                    signal = client_socket.recv(1024)
                    signal = signal.decode("utf-8")

                    #開始進行檔案傳輸
                    if signal == 'OK':
                        fileRecv(ANS_FILE_NAME, client_socket)

                #逾時處理
                except socket.timeout:
                    print('Server not responce.')
                    break

                #顯示出 ans.txt 的內容
                f = open(os.getcwd() + '/' + ANS_FILE_NAME, 'r')
                for lines in f:
                    print(lines, end='')
                f.close()
                calc_mode = 0
    #keyboard interrupt處理
    except KeyboardInterrupt:
        print("\nBye~")
        client_socket.close()
        quit()






