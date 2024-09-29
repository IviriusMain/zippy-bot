# Zippy Discord Bot

Offical Discord Moderation Bot for the Ivirius Community

## Features✨
- Moderation Commands
   - Kick
   - Ban
   - Mute
   - Unmute
   - Warn
   - Purge
   - Create Role
   - Delete Role
   - Create Channel
   - Delete Channel
   - Edit Channel

## ⚙️ How to setup

#### Rename the `.env.example` file to `.env`

```bash
mv .env.example .env
```

Now open the `.env` file and add your discord bot `TOKEN` to the file.

#### Install dependencies

```bash
pip install -r requirements.txt
```

OR

```bash
pipenv install
```

#### Start the bot

Linux

```bash
python3 main.py
```
Windows

```ps
python main.py
```

## Tasks

- [ ] Change the bot prefix to `>>`
- [ ] Fix unban command
- [ ] Add a command to show the bot's ping
- [ ] Add links command to show all the links to all Ivirius Products
- [ ] Add Member Count command to show the member count of the server excluding bots
- [ ] Fix other commands which are not working
- [ ] Remove unused commands

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
