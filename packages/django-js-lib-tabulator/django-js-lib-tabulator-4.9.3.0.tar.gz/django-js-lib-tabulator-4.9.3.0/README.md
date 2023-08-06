# Tabulator Repackaged for Django

[Tabulator](https://tabulator.info/) packaged in a Django reusable app.


## Installation

    pip install django-js-lib-tabulator

## Usage

1. Add `"js_lib_tabulator"` to your `INSTALLED_APPS` setting like this::

       INSTALLED_APPS = [
           ...
           "js_lib_tabulator",
           ...
       ]

2. In your template use:
   
       {% load static %}
   
   ...
   
       <link rel="stylesheet" href="{% static "tabulator/css/tabulator.css" %}">

   ...
   
       <script src="{% static "tabulator/js/tabulator.js" %}"></script>
   


