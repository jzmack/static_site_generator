# ADGroupManager

[< Back Home](/)

Check out the GitHub link below for full documentation and source code. Or the full blog post for more detail on how this project came about.

- [Link to GitHub repo](https://github.com/jzmack/ADGroupManager)
- [ADGroupManager Blog](/projects/ADGroupManager/blog)

### Overview

This project is a PowerShell module automates adding long lists of users to specific AD groups, replacing a slow and painful manual process. In addition its main purpose of adding users to groups, you can also verify if users are a part of a group and remove them from a group if needed.

Example adding 5 users:

```
PS C:\Users\mackinjz> AddToGroup -list -group "WLAN Users"
Successfully added User1 (user) to the WLAN Users group.
Successfully added User2 (user) to the WLAN Users group.
Successfully added User3 (user) to the WLAN Users group.
Successfully added User4 (user) to the WLAN Users group.
Successfully added User5 (user) to the WLAN Users group.
```

### Why I made this

Our previous process managing AD group memberships was time-consuming, click intensive, and exhausting for a long list of users. See the next section to see the stats on how much time is saved. This module serves as a great example of how putting in some up front work to automate a task can return long term dividends.

### Time saving impact

- **Manually:** It takes **~81s** for the first user and **~21s** per additional user

- **Scripted:** Processes **~5 users/sec**

- **Real Example:** 189 users would've taken **~64m** manually vs. **~40s** scripted

- **Summary:** Running the script is **~96%** faster than doing this manually, resulting in ~**98%** less time adding users to groups

![Speed UP](/images/speed-up-factor.png)
