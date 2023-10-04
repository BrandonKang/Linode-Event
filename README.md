# Receive Linode Event Alerts via Slack Channel

Linode event notifications are primarily received via email. Since Linode uses the email address provided during registration, these notifications often arrive at work email addresses. Therefore, Linode event emails may be perceived as spam by the end-users and are often overlooked when mixed with work-related emails. 

![email_off](/images/linode_event_emailoff.png)

Additionally, event emails provide a limited view of cloud resource history, making it impossible to access historical data for specific resources. They only contain information about events that occurred at a particular time.

Therefore, I began to consider receiving Linode events through Slack instead of my work email. Using Python coding along with Linode API and Slack API, I was able to implement this solution effortlessly. As a result, I was able to implement the desired functionality after investing a few hours. 

![slack_screenshot](/images/linode_event_slackscreen.jpg)

What's more, receiving events through Slack channels provides much more visibility compared to email. To run this code Seamlessly, you need to prepare a Linode instance and prepare an environment in advance where Python and Slack Client functions can run.

![backend_logo](/images/linode_event_backendlog.jpg)

To keep a Python code running on a cloud virtual machine (VM) even after the VM restarts, you can use various methods, including process managers, init scripts, and containerization. The choice of method depends on your expertise on Linux, cloud instance types and requirements. Here are a few common approaches:

Use a Process Manager  
On Linux VMs, you can use process managers like 'system.md', 'init.d' or 'Upstart' to manage and automatically restart your Python script as a system service. Create a custom service configuration file that specifies how your Python script should run and restart. These files are usually placed in for .

Use a Batch Job Scheduler  
If your Python script is meant to run periodically, consider using a batch job scheduler like . You can create a cron job that runs your script at specified intervals. This approach is suitable for tasks like data backups, periodic data processing, and more.

Use Supervisor  
Supervisor is a process control system that allows you to monitor and manage processes, including your Python script. You can install Supervisor and create a configuration file for your script, which ensures it is restarted if it exits unexpectedly.

Use Containerization (Docker & K8s)  
You can containerize your Python script using Docker and run it as a Docker container. Docker containers can be configured to restart automatically when the host system restarts. This approach provides isolation and portability. Once you have docker images, it's easy to deploy it on K8s for more stability and auto-scaling.

Choose the method that best suits your environment and requirements. Keep in mind that the specific implementation details may vary depending on your VM's OS. Additionally, ensure that you handle any required dependencies and environment variables properly to keep your Python script running smoothly.

It offers clear information and direct links to the resources, making it easy to quickly identify the resources where events occurred. Additionally, I appreciate the ability to access past event information through a single fixed Slack channel. Typically, Event APIs only provide data for up to 90 days, but using Slack allows access to data beyond that time frame.
