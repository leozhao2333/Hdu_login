# Hdu_login

This script is forked from [xia0ji233's blog](https://xia0ji233.pro/2021/12/08/%E6%A0%A1%E5%9B%AD%E7%BD%91%E6%A8%A1%E6%8B%9F%E7%99%BB%E5%BD%95/):paperclip:

And make some modifications to suit HDU login.

## Instruction

1. ``pip install -r requirements.txt``
2. Using ``Save_Password_to_file.py`` to save password
3. Edit ``srun_login.py`` for your account id
4. Enjoy it:wink:.

------

## Example for Unix-like system

1. Create script:

   ````bash
   #!/bin/bash
   /path/to/venv/bin/python /path/to/srun_login.py
   ````

2. Add running permission:

   ````bash
   chmod +x ./srun_login.sh
   ````

3. Edit service file ``/etc/systemd/system/srun_login.service``:

   ````bash
   [Unit]
   Description=Run srun_login.py at startup
   After=network.target
   
   [Service]
   ExecStart=/home/your_location/srun_login.sh
   WorkingDirectory=/home/your_location
   Restart=on-failure
   User=your_username
   
   [Install]
   WantedBy=multi-user.target
   ````

4. Enable service and run it:

   ````bash
   sudo systemctl enable srun_login.service
   sudo systemctl start srun_login.service
   ````

5. Check service status:

   ````bash
   sudo systemctl status srun_login.service
   ````

