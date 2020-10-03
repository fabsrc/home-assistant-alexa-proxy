# Home Assistant Proxy for Amazon Alexa

> A lightweight Lambda function for proxying requests from an Amazon Alexa skill to [Home Assistant](https://home-assistant.io/).

## Requirements

- **Amazon Developer** account
- **AWS** Account
- Public **Home Assistant** URL (must be secured with TLS)
- Home Assistant **Alexa Smart Home** component configuration

Also see https://developer.amazon.com/de/docs/smarthome/understand-the-smart-home-skill-api.html and https://www.home-assistant.io/components/alexa/#smart-home

## Configuration

- `HASS_URL`: URL to Home Assistant (e.g. `https://your-home-assistant-url.io`)
- `BEARER_TOKEN`: Long lived acces token (optional)
- `VERIFY_SSL`: Has to be false for self signed certificates. (default: `true`)

## Setup

1. Create a new **Amazon Alexa** skill on https://developer.amazon.com/alexa/console/ask/create-new-skill

   1. Enter a **Skill name**, e.g. "Home Assistant"
   2. Set your **Default language**
   3. Select **Smart Home** as model
   4. Click **Create skill**

2. Create an **AWS Lambda** function on https://console.aws.amazon.com/lambda/home#/create [in your AWS region](https://developer.amazon.com/de/docs/smarthome/steps-to-build-a-smart-home-skill.html#configure-the-smart-home-service-endpoint)

   1. Select **Author from scratch**
   2. Enter a function name, e.g. "home_assistant_proxy"
   3. Select **Python 3.7** as runtime
   4. Select a **lambda role**, e.g. "lambda_basic_execution"
   5. Click **Create function**

3. Configure **AWS Lambda** function

   1. Copy and paste the code from **hass_proxy.py** into the function code editor
   2. Add a **HASS_URL** environment variable which is set to the public base URL of your Home Assistant, e.g. "https://your-home-assistant-url.io"
   3. (optional) If you are using a self signed certificate for your Home Assistant, set the **VERIFY_SSL** environment variable to `false`
   4. Add **Alexa Smart Home** trigger
      1. Enter the **Skill ID** from your Alex skill in the **Application ID** field
      2. Select **Enable trigger**
      3. Click **Add**
   5. Click **Save**

4. Configure **Amazon Alexa Skill**
   1. Enter the **ARN** of the AWS Lambda function
   2. Click **Save**
   3. Click **Setup Account Linking**
      1. In **Authorization URI** enter the authorize URI of your Home Assistant, e.g. "https://your-home-assistant-url.io/auth/authorize"
      2. In **Access Token URI** enter the access token URI of your Home Assistant, e.g. "https://your-home-assistant-url.io/auth/token"
      3. Enter a redirect URL of Amazon Alexa as **Client ID**, e.g. "https://layla.amazon.com" (see **Redirect URLs**)
      4. Enter anything in **Client Secret** (is not used by Home Assistant)
      5. Select "HTTP Basic" as **Client Authentication Scheme**
      6. Add any **Scope**, e.g. "API" (is not used by Home Assistant)
      7. Click **Save**
5. Activate your Skill in the Amazon Alexa app or in the web interface
6. Discover devices

## Differences to [Haaska](https://github.com/mike-grant/haaska)

- Makes use of Home Assistant's [Authentication API](https://developers.home-assistant.io/docs/en/auth_api.html). There is no need to configure an oAuth provider or to create a long lived token.
- No dependencies to additional Python packages. It is not necessary to create a deployment package and upload it to AWS Lambda. Just copy the code from the `hass_proxy.py` file and paste into the AWS Lambda function editor.
- No config files. All configuration is done using environment variables.
