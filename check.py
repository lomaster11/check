import time
from threading import Thread
import requests, ctypes


#ctypes.windll.kernel32.SetConsoleTitleW("Private key Checker v1.0 | Total - 0.0$")


threadc = int(input("Введи количество потоков: "))
base = input("Введи путь к базе: ")
data = open(base, "r").readlines()
with open(base) as n:
    line_count = 0
    for line in n:
        line != "\n"
        line_count += 1
print('Total Addresses Loaded and Checking : ',str (line_count))

def divide(stuff):
    return [stuff[i::threadc] for i in range(threadc)]

def checker(data):
    total = 0.0
    count1 = 0
    for line in data:
        try:
            #private_key =str(line.replace("\n", ""))
            acct = line.strip()
            try:
                #print(f"{acct}")
                json_bal = requests.get(f"https://openapi.debank.com/v1/user/total_balance?id={acct}").json()
                total = float(total) + float(json_bal['total_usd_value'])
                #ctypes.windll.kernel32.SetConsoleTitleW(f"Private key Checker v1.0 | Total - {total}$")
                count1+=1*int(threadc)
                #print(f"\nAddress: {acct}\nFull Balance: {json_bal['total_usd_value']}\n-----------------------------------")
                #print(f"Checked: {count1}/{line_count}")
                print("Checked:", count1, sep=' ', end='\r', flush=True)
                #open(base, "w").write(line)
                if float(json_bal['total_usd_value']) > 100.0:
                    save = open("Results.txt", "a").write(
                        f"{acct}\n")
            except Exception as e:
                print(e)
                print("API Error , sleep 5s...")
                time.sleep(5)
                try:
                    json_bal = requests.get(
                        f"https://openapi.debank.com/v1/user/total_balance?id={acct}").json()
                    #print(json_bal["total_usd_value"])
                    #print(f"Address: {acct.address}\nFull Balance: {json_bal['total_usd_value']}\n-----------------------------------")
                    #print("Checked:", count1, end="")
                    #open(base, "w").write(line)
                    if float(json_bal['total_usd_value']) > 100.0:
                        save = open("Results.txt", "a").write(
                            f"{acct}\n")
                except Exception:
                    error = open("Errors.txt", "a").write(f'{acct}\n')
                    pass
                pass
        except Exception:
            pass


threads = []


for i in range(threadc):
    threads.append(Thread(target=checker,args=[divide(data)[i]]))
    threads[i].start()
for thread in threads:
    thread.join()
