# Week 0 — Billing and Architecture

## Conceptual Architecture Design using lucid charts
![Architecture Design](/_docs/assets/11DAF296-FBB0-470F-9C1B-3AF23A45814B.jpeg)
> You can find the corresponding [lucidchart] at: (https://lucid.app/lucidchart/9e9f32ac-53d3-4a89-94b2-a37ebf7bb20c/edit?invitationId=inv_2028d60d-80aa-4d58-b18f-e8ee3f552920).

## Installing AWS CLI

For installing the aws-cli on macOS, I have followed the steps mentioned below:
1. Downloaded the aws-cli package using curl command:
> $ curl <"https://awscli.amazonaws.com/AWSCLIV2.pkg"> -o "AWSCLIV2.pk"
2. After downloading the aws-cli package using curl. Run the standard macOS installer command
> $ sudo installer -pkg ./AWSCLIV2.pkg -target /
3. If there isn't any errors in the installation logs. verify the installation using
> which aws

![The output looks similar to:!](/_docs/assets/71BADFF0-064D-485B-8CA5-31FC5D1AD74E_4_5005_c.jpeg "The output looks similar to:")

### Checking the caller identity using CLI command

> aws sts get-caller-identity

![Caller Identity!](/_docs/assets/DE6822C5-D8BD-4816-852A-71120D427FAF_4_5005_c.jpeg "Caller Identity")

## Creating the Billing Alarm

* I have created two billing alarm. First billing alarm is created using AWS management console and the second alarm is created using aws-cli command.

![Billing Alarm!](/_docs/assets/45D01736-597B-4265-B6DA-43F44D3553D3.jpeg "Billing Alarm")


## Creating a Budget
* I have created two monthly budgets similar to billing alarms. First budget is created using AWS management console and the second budget is created using aws-cli command.

![Monthly Budgets!](/_docs/assets/223AF4A9-FA45-434E-A735-8FF05F5B202C.jpeg "Monthly Budgets")

