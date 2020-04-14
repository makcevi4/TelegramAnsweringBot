#Answering Bot
![logo](logo.png)

##Description
>Attention! In this case, an «answering bot»  is meant as an answering machine

**Mission** of answering bot:

This bot was designed for people who have a serious social circle 
and they need an answering machine that will answer in their absence.

**Advantages** of answering bot:
1. Telegram bot control (thoughtful menu)

2. Two modes of operation: all users, friends 
    * If you use the «All users» mode, then the answering bot will respond to all users who write in your absence
    * If you use the «Friends» mode, then the answering bot will only respond to users who are in your friends list.
    And also friends have the ability to send a message marked «!IMPORTANT»

3. Login Data Protection

4. Ignore people who are on the answering bot blacklist

5. Protecting answering bot control from other people

**In the future**, it is planned to introduce:

1. Setting message by user

2. Auto delete unnecessary messages and commands in the control panel

3. Automatically turn off notifications when the answering bot is running

4. Logging

5. Auto-blocking users (when the answering bot is active), who write a lot of messages

6. Filtering and automatic removal of unwanted messages

7. Add/Remove user to friend list/blacklist in control panel

## Requirements
* Internet
* Telegram account
* Python 3+ version
* Installed pip package management tool for Python
* The presence of a remote server (for continuous operation)

## Used modules
* PyTelegramBotAPI
```angular2
$ pip3 install pyTelegramBotAPI
```

* Pyrogram
```angular2
$ pip3 install Pyrogram
```

* Cryptography
```angular2
$ pip3 install cryptography
```

All other modules should already be installed on your computer.
If you get the error "module not found", find module on the [PyPi](https://pypi.org)

## Usage
For the answering bot you need: Telegram app API and TOKEN, your Telegram ID, Telegram bot TOKEN
### Creating Telegram App
Visit [my Telegram applications](https://my.telegram.org/apps) and create an application.
After that, you will get access to view your **api_id** and **api_hash** from the application 
### Getting Telegram bot token
Open Telegram app (It can may be: desktop, mobile or web app) and looking for a bot with the nickname **@botfather**, and start a dialogue with it.

Create a bot using the command **/newbot** and give it a name, and username.
>Attention! Username must end in "bot".

After the name is selected, **@botfather** will send the bot token.
### Registration Data
Registration of data is an integral part of answering bot preparation, 
without this data, the answering bot will not work. So, registration is required!

To start registration, run the **register.py**
```angular2
$ python3 register.py
```
Then you can watch the interactive menu, which is responsible for registering different types of data.

**1. For login (answering bot)**

In order for the answering bot to work, it needs to log in to your account!

When you run the **register.py**, select «**1**» in the interactive menu, 
in order to proceed to the registration of login data.

The data you will need to enter:
1. ID, means **api_id** of your Telegram app
2. HASH, means **api_hash** of your Telegram app
3. PHONE, your **phone number** (means account number)
4. PASSWORD (is not necessary), **password** for your account (means, **two-step verification password**) if it is

>Attention! You have every right not to enter your two-step verification password!
>But for security reasons, your data is encrypted after registration ends. 


**2. For bot (control panel)**

The answering bot is controlled by a personal Telegram bot. 
For the answering bot control panel to work, you need to register the configurations.

When you run the **register.py**, select «**2**» in the interactive menu, 
in order to proceed to the registration of configurations

The data you will need to enter:
1. Your Telegram **ID**
2. Telegram bot **TOKEN**
3. Your **TIMEZONE**

**3. Additional**

Also you can add/remove an user to your friends list or blacklist.

#####- ADDING

To **add** a user to your **friends list**, select «**3**».
The data you will need to enter:
1. User **ID**
2. **Name** of user

To **add** a user to **blacklist**, select «**4**», you will need to enter only the ID of the user, which you want to block.

#####- REMOVING

To **remove** a user from the **list of friends**, select «**5**». 
You will need to enter the ID or Name of the user, which you want to delete.

To **remove** a user from the **blacklist**, select «**6**». 
You will need to enter only the ID of the user, which you want to delete.

## Run
>To uninterrupted work of the  bot, you can place it on the server (Heroku and etc.) using instructions from the internet.
>In this case, it describes how to start an answering bot in a virtual environment

**1**. Run Virtual Environment

How to install and create, see FAQ (below)

For example:
```angular2
$ source name_of_environment/bin/activate
```
**2**. Go to the directory where this repository was cloned

For example:

```angular2
cd /home/user/repositories/TelegramAnsweringBot
```

**3**. Run the «run.py» script
```angular2
python3 run.py
```

**4**. Bot launch

Open Telegram app and go to the bot that you created (as an answering bot control panel)
activate the bot using the **/start** command


**5**. Activating an answering bot

Open the **control menu** (if not open), 
go to the section «**Managing**», 
click on the corresponding button («**ON/OFF**») responsible for activating an answering bot.

**6**. **DONE**

You can go do something or sleep :)

## FAQ
Q: Where can I find my ID?

A: In Telegram you can use **@userinfobot**. Just send him a message and he will send you your ID.

##
Q: Where can I find ID of my interlocutor?

A: Same way as finding your own ID. Forward the message of your interlocutor and bot will send you his ID.
##
Q: How to get status of answering bot?

A: Telegram App > Answering bot control panel > «**Managing**» > «**Status**».
##
Q: How to install or create Virtual Environment?

A: Look [here](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b).
##
Q: What format to enter timezone?

A: You must enter your continent, and after the slash specify the city (preferably the capital).
For example: «Europe/Kiev».
##
Q: How to set mode 'All users' or 'Friends'?

A: Telegram App > Answering bot control panel > «**Managing**» > «**Set mode**».
##
Q: How to contact the developer?

A: Telegram App > Answering bot control panel > «**Help**» > «**Contact with Developer**».
##
Q: How to see a friend list or blacklist?

A: Telegram App > Answering bot control panel > «**Registration**» > 
«**Show users from friends list**» or «**Show users from blacklist**».
##
Q: How to add an user to friend list or blacklist?

A: Unfortunately, the function of adding/removing users through the control panel is **temporarily** unavailable.
You can do it manually by running the **register.py** script.

##
Q: How to find out the name of the session?

A: Telegram App > Answering bot control panel > «**Managing**» > 
«**Show session name**» or «**Display all information in a message**».
##
Q: Where can I find messages that were sent marked as important?

A: Telegram App > Saved Messages
