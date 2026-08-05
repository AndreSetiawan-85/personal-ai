DOMAIN_SOURCES = {


    "news": [

        "reuters.com",

        "openai.com",

        "blog.google",

        "microsoft.com",

        "techcrunch.com",

    ],



    "travel": [

        "booking.com",

        "tripadvisor.com",

        "airbnb.com",

        "lonelyplanet.com",

    ],



    "shopping": [

        "amazon.com",

        "bestbuy.com",

        "notebookcheck.net",

        "rtings.com",

    ],



    "food": [

        "seriouseats.com",

        "allrecipes.com",

        "cookpad.com",

        "bbcgoodfood.com",

    ],



    "coding": [

        "github.com",

        "stackoverflow.com",

        "python.org",

        "developer.mozilla.org",

    ],



    "finance": [

        "reuters.com",

        "bloomberg.com",

        "coindesk.com",

    ],



    "health": [

        "mayoclinic.org",

        "webmd.com",

        "who.int",

    ],

}



def get_priority_sources(domain):


    return DOMAIN_SOURCES.get(
        domain,
        []
    )