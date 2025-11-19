# Aruba AirWave SSL Auto-install

[< Back](/projects)

## Overview

This project is a mostly-automated solution for installing SSL certificates on Aruba AirWave servers. To accomplish this, I used Python and the APIs on Aruba AirWave, which has one API specifically for installing SSL certs. I say mostly automated because at my organization, there is a separate team that manages and approves new certs for web servers, and that first step of obtaining a cert for renewal could not be automated. Had we been managing the certs with Aruba Clearpass, then this could have easily been a fully automated self-serve process. So this solution accounts for that single restraint and aims to make deploying new SSL certs on these servers as efficient as possible. 

![AirWave SSL Cert visual](/images/airwave-ssl-cert.png)

## Why I made this

Since we only have to update the certificates once per year, there isn't significant time savings like with my other project, the [ADGroupManager PowerShell module](/projects/ADGroupManager). So this one is more for the "because it's cool" factor, and at the same time, it didn't take a ton of effort to build it. Also, we have over a dozen AirWave servers in our fleet and I don't know, doing something a dozen times in a row gets boring. And hey, when it is that time of year again, it'll be super easy and take less than 5 mintutes.

## How it works

The first step here is the only manual requirement, the rest of this section will go over how the Python script works with the SCP server and AirWave APIs. Refer to the picture above to reference.

### Obtaining the new certificate

As I mentioned in the Overview section, this solution is specific to the organization that I work at. Therefore, I had to request the new certificate throught the MMC of a domain connected Windows Server that had rights to do so. This is the only required step that could not be automated here. Once the cert was generated or renewed, I save it to a local folder on the server that I will retrieve later on using SCP, noting the name of the certificate file.

### Transferring file from Windows Server to local machine (or server)

This script could have been ran from my local laptop, but instead I'm using an Ubuntu Linux server that I have other scripts and automations set up on. So the laptop in the picture above actually represents my Linux server. To retrieve the newly generated SSL certificate from the Windows, I'm using SCP. The Windows Server has an SCP service running on it that I can use, and the SCP user's home directory is where I saved the cert as a **.pfx** file.

In terms of Python, I'm using the `subprocess` module which can basically run CLI commands. See my full function below and note the `scp_command` variable. Also, note that the variables in all caps like `WIN_SERVER_IP` were global variables in this instance.

```
def transfer_cert_from_windows(cert_file_name):
    local_cert_path = f"./{cert_file_name}"
    print(f"[INFO] Copying {cert_file_name} from Windows ({WIN_SERVER_IP}) to local directory...")

    scp_command = f"scp {WIN_USERNAME}@{WIN_SERVER_IP}:{WIN_FILEPATH}{cert_file_name} {local_cert_path}"

    try:
        subprocess.run(scp_command, shell=True, check=True)
        print("[SUCCESS] Certificate successfully copied to current directory!")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] SCP transfer failed: {e}")
        exit(1)

    return local_cert_path
```

### Encoding the certificate

Once the certificate is copied over, it needs to be encoded in base64 format. The Aruba AirWave API documentation provides a shell command to do this, which is probably the easiest way to do this again using the `subprocess` module. I instead used the `base64` Python module to accomplish this. The function I used is as follows.

```
def encode_cert(file_path):
    print(f"[INFO] Reading the certificate file: {file_path}")
    
    try:
        with open(file_path, "rb") as cert_file:
            encoded_cert = base64.b64encode(cert_file.read()).decode("utf-8")  # Convert bytes to string
        print("[SUCCESS] Certificate file successfully encoded to base64 format.")
        return encoded_cert
    except FileNotFoundError:
        print("[ERROR] Certificate file not found. Please check the file path.")
        exit(1)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while encoding the certificate: {e}")
        exit(1)
```