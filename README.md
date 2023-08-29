# Prerequisites
- OpenVPN Client 2.4.6
- Amazon AWS Account

# Set Up EC2 Instance
1. Go to [AWS EC2](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Home)
2. Click on `Launch Instance`
3. Choose a name for the instance
![](attachments/Pasted%20image%2020230828220315.png)
4. Select Ubuntu as OS image
![](attachments/Pasted%20image%2020230828220342.png)
5. Select the instance type (based on hardware requirements)
![](attachments/Pasted%20image%2020230828220433.png)
6. Create a `Key Pair`.
![](attachments/Pasted%20image%2020230828220554.png)
7. Save the file `.pem` and keep it accesibble
8. On Network setting click on `Advanced Settings`
9. Disable `Auto-assign public IP`
![](attachments/Pasted%20image%2020230828220949.png)
10. Create a new security group
11. And set the next settings
![](attachments/Pasted%20image%2020230828221249.png)
12. Click on Launch Instance
13. Now go to [EC2 Elastic IPs](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Addresses:)
14. Click on Allocate Elastic  IP address
15. And click on Allocate
16. Now Select the IP and click Actions > Associate Elastic IP address
![](attachments/Pasted%20image%2020230828221917.png)
17. Choose the instance and their Private IP address and click Associate.
![](attachments/Pasted%20image%2020230828222025.png)

Now you can log in by SSH to the instance using the `.pem` file
```shell
ssh -i "gns3-server-key.pem" ubuntu@ec2-54-147-136-36.compute-1.amazonaws.com
```

# General Steps
## Install GNS3 on Cloud (Azure VM, EC2, etc)

### Steps:

1. Create the remote server
* To create a Linux virtual machine in the Azure portal follow these [steps](https://docs.microsoft.com/en-gb/azure/virtual-machines/linux/quick-create-portal?WT.mc_id=UI_empg)
* To create Amazon EC2 Linux instance follow these [steps](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)

1. Open port `1194` for the remote server.

2. Install GNS3 on a remote server
Commands as `root`:
```shell
cd /tmp
curl https://raw.githubusercontent.com/GNS3/gns3-server/master/scripts/remote-install.sh > gns3-remote-install.sh
bash gns3-remote-install.sh --with-openvpn --with-iou --with-i386-repository
```
Explanation for commands is provided [here](https://docs.gns3.com/docs/getting-started/installation/remote-server).

3. Reboot the instance
```shell
reboot now
```

4. Download the certificate. You can also find the certificate in `/root/client.ovpn`. You can also use `scp` command. First copy `/root/client.ovpn` to `/home/<remote_user>`, then you can use scp to copy it locally.
```shell
scp <remote_user>@<remote_ip>:/home/<remote_user>/client.ovpn client.ovpn
```

5. VPN connection on local Linux
```shell
sudo apt-get install openvpn
sudo openvpn --config client.ovpn --auth-retry interact
```

6. VPN connection on Windows
  Download and install OpenVPN for [Windows](https://openvpn.net/index.php/open-source/downloads.html).

  * Click on “Show Hidden Items” in the Taskbar
  * Right-click on “OpenVPN-GUI”, and select “Import file”
  * Select the .ovpn file you downloaded, and click “Import”
  * Right-click on “OpenVPN-GUI” again, and select “Connect”

>My recommended [OpenVPN Version 2.4.6](https://swupdate.openvpn.org/community/releases/openvpn-install-2.4.6-I602.exe)


1. If the VPN works, this page should work: http://172.16.253.1:3080/

# AWS IAM

Policy to only Allow Stop and Start EC2 Instances
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": [
                "arn:aws:ec2:*:078462726356:instance/*",
                "arn:aws:license-manager:*:078462726356:license-configuration:*"
            ]
        }
    ]
}
```
