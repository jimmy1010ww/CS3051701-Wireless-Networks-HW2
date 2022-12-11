import  socket  
import os
import time

# Serve Info
HOST = '127.0.0.1'
PORT = 12000
calc_mode = 0

#File IO
ANS_FILE_NAME = 'Ans.txt'
INPUT_FILE_NAME = 'Testcase.txt'


def initServerSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) 
    s.listen(5)
    print (f"Listening on Ip:{HOST}\nPort:{PORT}\n===================================")
    return s

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

def doCalc(expression):
    try:
        expression = expression.replace("^","**")
        Ans=str(eval(expression))
    except:
        Ans='Invalid input'
    return Ans


if __name__ == "__main__":
    os.system("clear")

    try:

        server_cocket = initServerSocket()
        
        while True:
            print("Wait for connection...")
            client,addr = server_cocket.accept()
            print (f"Connected from: {addr}")

            with client:
                while True:

                    # 初始化狀態，準備接受用戶端模式資料
                    if calc_mode == 0:
                        #接收用戶端傳送過來的資料
                        recv_data = client.recv(1024)
                        #用 UTF-8 解碼
                        decode_data = recv_data.decode("utf-8")

                        #處理不正確發送請求
                        if decode_data.isnumeric():
                            calc_mode = int(decode_data)
                        elif decode_data == 'q' or decode_data == 'Q':
                            print("Client quit.")
                            client.close()
                            print("\n===================================")
                            break
                        else:
                            print(f"Client sent invalid data => {decode_data}")
                            continue

                        #回傳 OK 給用戶端，表示伺服器準備好接受資料
                        print(f"Client choose mode: {calc_mode}")
                        client.send("OK".encode("utf-8"))

                    # 模式 1: 手動（單行）輸入
                    elif calc_mode == 1:
                        recv_data = client.recv(1024)
                        decode_data = recv_data.decode("utf-8")

                        if decode_data == 'MODE_QUIT':
                            print("Exit mode 1.")
                            calc_mode = 0
                            continue
                        else:
                            print(f"Client sent data => {decode_data}")
                            Ans = doCalc(decode_data)
                            if Ans == "Invalid input" or Ans == '':
                                print("Client sent invalid data.")
                                client.send("Invalid input".encode("utf-8"))
                            else:
                                print("Server sent data => {:.2f}".format(float(Ans)))
                                client.send(doCalc(Ans).encode("utf-8"))

                    elif calc_mode == 2:
                        #接收 Testcase.txt
                        fileRecv(INPUT_FILE_NAME, client)

                        #計算
                        f_input = open(INPUT_FILE_NAME, 'r')
                        f_ans = open(ANS_FILE_NAME, 'w')

                        for lines in f_input:
                            f_ans.write(doCalc(lines) + '\n')
                        
                        f_input.close()
                        f_ans.close()

                        client.send("OK".encode("utf-8"))
                        fileSend(ANS_FILE_NAME, client)

                        print("Exit mode 2")
                        calc_mode = 0
    except KeyboardInterrupt:
        print("Server quit.")
        client.close()
    except:
        print("Server error.")
        quit()









            