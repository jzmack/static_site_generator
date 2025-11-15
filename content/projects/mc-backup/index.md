# Mobility Conductor Backup Solution

[< Back](/projects)

### Overview

This is a fully automated backup solution for using Python, SCP, and the APIs of the Aruba Mobility Conductors. In our environment, we have several conductors that manage hundreds of Managed Devices (MDs), which are WLAN controllers. The goal of this project was to ensure that the flash storage and full configuration of each Mobility Conductor was backed in a secure location up every week, and that the process was fully automated.

![MC-Backup](/images/mc-backup.png)

### Why I made this

You need backups for your important network infrastructure devices, it's as simple as that. Having that solution done in a fully automated manor is preferable. Mistakes will be limited and if a backup should fail for any reason, we will be notified.

### Impact

Peace of mind. In our organization, this solution was previously done manually and at an irregular pace. Now, a cron job runs once a week and we don't have to worry whether or not our important devices are backed up.

### How it works

Refer to the image above to help follow along these next 4 steps. These are the core steps of the automation. Below them, I'll also be documenting how the cron job is configured, as well as how the email notifications are set up when jobs complete.

#### Step 1: Logging into the conductor

The API endpoint for this is `/v1/api/login`

This endpoint requires that a `username` and `password` be passed as parameters.

Using a GET to this endpoint, the conductor will return a JSON object containing an X-CSRF-Token and Cookies, which can be used and passed into further API calls.

Here's my full function for logging in:

```
def login(ip, username, password):
    print(f"Attempting to log into {ip}...")
    r = requests.get(url="https://" + ip + f":4343/v1/api/login?username={username}&password={password}", verify=False)
    logindata = r.json()
    token = logindata["_global_result"]["X-CSRF-Token"]
    uid = logindata["_global_result"]["UIDARUBA"]
    cookies = {"SESSION": uid}
    print(logindata["_global_result"]["status_str"])
    return(token, cookies)
```

#### Step 2: Creating a backup running config and flash

These is kind of two steps lumped into one, but I'll explain both. First we need a function to make POST requests to the conductor. I'll specify which parameters we will set further down.

Here's my function for making POST requests:

Now we need to create a backup of the running config of the Conductor on to the flash of the device. To do this, the endpoint is `/v1/configuration/object/copy_running_flash`. This is a POST request and in the body of the request, you can specify the filename of the backed up config file. Here's my function for this:

Next, we create the flash backup with the following endpoint: **/v1/configuration/object/flash_backup**. Similar to the last endpoint, we will make a POST request, and in the body we are specifying what we are backing up and what we want the filename to be. See the function below to see how I structured the parameters. Note that **flash** for filename actually becomes **flash.tar.gz**. Had to learn that one the hard way.

```
def create_flash_backup(ip, hostname, token, cookies):
    api_endpoint = r"/v1/configuration/object/flash_backup"
    body = {
        "backup_flash": "flash",
        "filename": "flash"
        }
    params = {"config_path": "/md"}
    return api_post(api_endpoint, token, cookies, ip, body, params)
```


#### Step 3. Transfer files to remote server using SCP

Now that the files that I want to back up are created, it's time to securely copy them to a remote server. In my case, we had a VM running Windows Server 2019 and an SCP service running. To authenticate, I used an account local to the SCP service. I configured the SCP user to have a home directory exactly where I want the backup files to live.

On the Conductor, the handy API endpoint is **/v1/configuration/object/copy_flash_scp**, which is used twice within the same function using two different bodies in the POST requests (one for each file). The resturning result is either a string saying it was a success or a failure. Note the differences between the source and destination filenames. I used the hostname to keep track of which Conductor the backup belonged to.

#### Step 4: Cleanup and logout

Now the files are sent over to the remote server, we can safely delete the tar file generated containing the flash backup. The config backup can still and will just be overwritten everytime the script runs.

On the Conductor, the endpoint is **/v1/configuration/object/tar_flash_clean**, which will delete any .tar files living in the directrory you specify. In our case we're cleaning the **/md** directory on the Conductor.

Here's the function I wrote to do that:

Lastly, we log out of the conductor by making a GET to the **/v1/api/logout** API endpoint. Here's the code function I made for that. In this, I use an **api_get** function that look very similar to the function to login from **Step 1**

#### Email notifications

After the flash is cleaned, we can check the JSON responses from the **/v1/configuration/object/copy_flash_scp** endpoint where we copied the two files over. In this script, I have those responses store in memory so I can check them here. What we are looking for in the JSON response is the value within the **status** key. If the status is **SUCCESS**, then we mark that one as good. Otherwise, it's marked as a failure.

All of the successes (and hopefully non failures) get composed into an email using the **email** and **smtplib** Python modules. Our organization has an accessible SMTP Relay server so it made it very simple to use that to send my team an email.

Here's what that function looks like:

#### Cron Job



### References

- https://arubanetworking.hpe.com/techdocs/ArubaOS-8.x-Books/AOS-8.x-API-Guide.pdf

- The swagger interface on the Conductors are super helpful too