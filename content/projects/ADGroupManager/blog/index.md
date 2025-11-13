# ADGroupManager Blog post

[< Back Home](/)

## Intro

This module came about as our organization was diving deeper into network segmentation to tighten up security. Certain devices needed to use service accounts, be in specific VLANs, AD groups, etc. As a result, my team, who supports the WLAN across the enterprise, would start getting requests that service accounts or device accounts be added to a certain AD group to get access to the network resources that they need over the Wi-Fi. 

A lot of times these tickets would have long lists of users, sometimes over 100. So we needed a quick and efficient to add long lists of users to a group that we specify, because manually doing this in AD Users & Computers was painful and took way too long. On top of that, we would need a way to verify that the user in in the correct group which this module also includes.

## Time Saved

I calculated how long it would take for us to manually add users in Active Directory and here were my results. These are approximations but still gives a good idea of how much time is saved using this script vs. doing this task manually.

The approximate time it takes to RDP into a server that has AD Users and Groups, open AD, find the user, and add them to a group takes about **81 seconds** to add the first users, and then about **20 seconds** for every additional user. 

All it takes to run the script is to open PowerShell, populate the userlist.txt file with the users, and run it with the correct parameters. The script can add about **5 users per second**.

To give an example, we recently had a request to add 189 users to a group. Doing this manually would have taken approximately **3841 seconds** or **64 minutes**. Running the script took about **40 seconds** to add all the users. Therefore, the script is faster by about a factor of **96%** resulting in **98% time saved**. With the amount of requests we get like this, using this script is paying off dividends in the form of valuable time.

## Ease of use

This module is availabe for free on the PowerShell gallery. There are a few prerequisites such as having delegated control to the OU you need and a computer with RSAT so you can access AD Users and Computers. 

I was able to get people who never scripted before to install and use this module to save them time. Here's a real email sent out to my team.

```plain
Thanks to Jake and his wonderful AD scripting tool what would’ve taken a decent amount of time took less than a minute. 189 accounts added just like that.
```

This is why I do it. To make tools that aren't just useful for me, but to save someone else their most valuable time. 