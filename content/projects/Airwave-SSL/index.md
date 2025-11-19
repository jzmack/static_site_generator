# Aruba AirWave SSL Auto-install

[< Back](/projects)

## Overview

This project is a mostly-automated solution for installing SSL certificates on Aruba AirWave servers. To accomplish this, I used Python and the APIs on Aruba AirWave, which has one API specificly for installing SSL certs. I say mostly automated because at my organization, there is a separate team that manages and approves new certs for web servers, and that first step of obtaining a cert for renewal could not be automated. Had we been managing the certs with Aruba Clearpass, then this could have easily been a fully automated self-serve process. So this solution accounts for that single restraint and aims to make deploying new SSL certs on these servers as efficient as possible. 

![AirWave SSL Cert visual](/images/airwave-ssl-cert.png)

## Why I made this

Since we only have to update the certificates once per year, there isn't significant time savings like with my other project, the [ADGroupManager PowerShell module](/projects/ADGroupManager). So this one is more for the "because it's cool" factor, and at the same time, it didn't take a ton of effort to build it. Also, we have over a dozen AirWave servers in our fleet and I don't know, doing something a dozen times in a row gets boring. And hey, when it is that time of year again, it'll be super easy and take less than 5 mintutes.

## How it works

The first step here is the only manual requirement, the rest of this section will go over how the Python script works with the SCP server and AirWave APIs.

### Obtaining the new certificate

As I mentioned in the Overview section, this solution is specific to the organization that I work at. Therefore, I had to request the new certificate throught the MMC of a domain connected Windows Server that had rights to do so. This is the only required step that could not be automated here. Once the cert was generated or renewed, I save it to a local folder that I will retrieve later on using SCP, noting the name of the certificate file.

### 

