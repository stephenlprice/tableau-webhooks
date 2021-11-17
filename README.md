# Tableau & Twilio via Webhooks

A project demonstrating the use of Tableau's [Webhooks API](https://www.tableau.com/developer/tools/webhook-api) and [Twilio](https://www.twilio.com/) to send notifications to a site or server administrator upon failed data source refreshes.

The app is capable of sending SMS, WhatsApp and perform phone calls when certain events take place on a Tableau Server or Tableau Online site.

![webhook description](assets/images/webhooks-vs-apis.png)
##### *source: [CleverTap: What Are Webhooks? And Why Should You Get Hooked?](https://clevertap.com/blog/what-are-webhooks/)*

</br>

## Dependencies

This project was built with [Anaconda](https://www.anaconda.com/), therefore the development environment can be cloned from the `environment.yml` file. Most dependencies are installed with `conda` while the last three are installed with `pip3`.

```yaml
name: tableau-twilio
channels:
  - defaults
dependencies:
  - python=3.8.8
  - flask=2.0.2
  - gunicorn=20.1.0
  - pip=21.2.4
  - pip:
    - python-dotenv==0.19.2
    - twilio==7.3.0
    - tableauserverclient==0.17.0
prefix: /Users/stephenlprice/anaconda3/envs/tableau-twilio
```

## Environment Variables




