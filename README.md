# Overview

This software is the first time I'm programming something to send data between two computers. This is an important first step for me, as communicating between computers is vital for almost all consumer software. 

This software is a basic network file manager. The files are stored on the server side in the "files" folder. On the client side, you have two folders, "files" and "uploading". The "files" folder is where files that you download from the server go to, and "uploading" is where you can put files that you're going to upload to the server. 

With both the client and server software, you'll simply run the python file in a terminal. As expected, you need to first start the server side, then the client side, so that the client is able to connect to the server. There isn't anything to do on the server side once you've started it, as it's only there to hold the files and manage them. On the client side, you'll be given options in the terminal for what action you want to perform next. 

My purpose of writing this software was to introduce myself to network programming. I wanted to create a basic server and client, and learn how to manage that connection, and send data between the server and client. 

[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

I decided to use the client-server architecture, as I felt this made the most sense for a this software. This way, the files are stored on the server and managed through the client. 

I am using TCP, and using port 2222. I set the IP address as the internal IP address of the computer running the server.

The messages sent between client and server are in binary. So, any messages in text need to be encoded and decoded as "utf-8". Files are generally received in packets of 4096 bytes in a loop until the end of file is reached. 

# Development Environment

I used VScode to program this software. 

This program was made in Python, utilizing the socket, socketserver, and os libraries. 

# Useful Websites

* [Python documentation for client](https://docs.python.org/3/library/socket.html)
* [Python documentation for server](https://docs.python.org/3/library/socketserver.html)
* [Python documentation for local OS file management](https://docs.python.org/3/library/os.html)

# Future Work

* Create a better interface
* Add an option to edit a file
* Add an option for uploading or downloading multiple files at once