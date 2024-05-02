# Bank of Charles Rewards.

The application is a flask app, and is designed to be unzipped and run in your Kali vm.

To setup, and run the app. Open your terminal in the directory that you have unzipped this source code to, and run the following command `. run-app.sh`.

The application will start and serve a website on http://localhost:5000

You can visit this site, and use Burpsuite to investigate requests, etc.

Ensure you are not connected to the VPN when runnign this exam, as you need Internet.

# Fixing the code

Flask is running in debug mode, and each time you make a change to a file, it'll update automatically.
