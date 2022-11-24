import  socket  
import os
import time

# Serve Info
HOST = '127.0.0.1'
PORT = 12000
calc_mode = 0

#File IO
ANS_FILE_NAME = 'ans.txt'
INPUT_FILE_NAME = 'Testcase.txt'


def initServerSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT)) 
    s.listen(5)
    print (f"Listening on Ip:{HOST}\nPort:{PORT}\n===================================")
    return s



if __name__ == "__main__":
    os.system("clear")

    server_cocket = initServerSocket()

    while True:
        print("Wait for connection...")
        client,addr = server_cocket.accept()
        print (f"Connected from: {addr}")

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

                    try:
                        decode_data=decode_data.replace("^","**")
                        Ans=str(eval(decode_data))
                    except:
                        Ans='NULL'
                    print('ANS => '+Ans)
                    client.send(Ans.encode("utf-8"))
            elif calc_mode == 2:
                print(os.getcwd() + '/' + INPUT_FILE_NAME)
                with open(os.getcwd() + '/' + INPUT_FILE_NAME,'wb') as f:
                    while True:
                        print ("Receiving...")
                        l = client.recv(1024)
                        f.write(l)
                        if len(l) < 1024:
                            break
                    f.close()
                print('receive done')
                calc_mode = 0







            