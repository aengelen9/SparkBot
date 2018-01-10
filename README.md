# CSV Spark Bot

This Python/Flask application allows a Cisco Spark Bot to bulk add participants to a Spark Space from a CSV file.

## CSV File Format

This application was designed for CSV files respecting this format:

```
First Name;Last Name;Email
```


## Getting Started

### Creating a Cisco Spark Bot

The first step would be to create a Cisco Spark Bot. Don't forget to copy the **Access Token** somewhere safe. Add the bot to the Spark Space where you want to add participants. The bot has to have the right to add participants into the space. Update the variables **BOT_TOKEN** and **SPACE_ID** in *app.py*.

### Hosting the App

The app needs to be hosted somewhere publicly accessible. For example, I use [Heroku](https://www.heroku.com/).

### Creating a WebHook

You need to create a WebHook that will send an HTTP POST message to *http://yourapp.com/sparkhook* when a message is addressed to the bot in the space.

You can create the WebHook from the Cisco Spark for Developers platform with these request parameters (using the bot's access token):

* resource - *messages*
* event - *created*
* filter - *roomId=SPACE_ID*

Your app should now be up and running.

## Resources

* [Cisco Spark for Developers](https://developer.ciscospark.com)
* [Heroku Dev Center](https://devcenter.heroku.com)
* [ciscosparkapi Documentation](https://ciscosparkapi.readthedocs.io)
* [#spark4devs Support Space](https://developer.ciscospark.com/support.html)
* [Python/Flask App on Heroku](https://realpython.com/blog/python/flask-by-example-part-1-project-setup)
* [Example Bots](https://ciscosparkambassadors.github.io/StarterKits)

