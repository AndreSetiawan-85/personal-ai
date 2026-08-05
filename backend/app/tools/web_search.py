from ddgs import DDGS

from app.services.source_validator import (
    filter_trusted_results
)





TRUSTED_SOURCES = {


    "reuters.com": 10,
    "openai.com": 10,
    "blog.google": 10,
    "microsoft.com": 10,
    "github.com": 10,
    "python.org": 10,
    "nature.com": 10,
    "arxiv.org": 10,


    "bbc.com": 8,
    "techcrunch.com": 8,
    "theverge.com": 8,
    "wired.com": 8,
    "cnn.com": 7,


    "allrecipes.com": 8,
    "foodnetwork.com": 8,

    "tripadvisor.com": 8,
    "booking.com": 8,


}





def calculate_trust_score(
    url: str
):

    if not url:

        return 0


    url = url.lower()


    for domain, score in TRUSTED_SOURCES.items():

        if domain in url:

            return score



    return 3






def build_search_query(
    query: str,
    category: str = None
):


    if category == "news":


        return (

            f"{query} "

            "site:reuters.com OR "
            "site:bbc.com OR "
            "site:techcrunch.com OR "
            "site:theverge.com"

        )




    if category == "food":


        return (

            f"{query} "

            "site:allrecipes.com OR "
            "site:foodnetwork.com"

        )




    if category == "travel":


        return (

            f"{query} "

            "site:tripadvisor.com OR "
            "site:booking.com"

        )




    if category == "coding":


        return (

            f"{query} "

            "site:github.com OR "
            "site:stackoverflow.com OR "
            "site:python.org"

        )




    if category == "shopping":


        return (

            f"{query} "

            "review OR comparison"

        )




    return query







def web_search(
    query: str,
    category: str = None,
    max_results: int = 5
):


    results = []



    search_query = build_search_query(
        query,
        category
    )




    try:


        with DDGS() as ddgs:


            search_results = ddgs.text(

                search_query,

                max_results=max_results

            )



            for item in search_results:


                source = item.get(
                    "href"
                )



                results.append(

                    {

                        "title":
                            item.get(
                                "title"
                            ),



                        "source":
                            source,



                        "snippet":
                            item.get(
                                "body"
                            ),



                        "trust_score":
                            calculate_trust_score(
                                source
                            )

                    }

                )





        # ranking trust score

        results.sort(

            key=lambda x:

                x.get(
                    "trust_score",
                    0
                ),

            reverse=True

        )





        # filter sumber

        filtered_results = filter_trusted_results(

            results,

            minimum_score=50

        )





        return {


            "query":
                query,


            "search_query":
                search_query,


            "category":
                category,


            "results":
                filtered_results


        }





    except Exception as e:


        return {


            "query":
                query,


            "search_query":
                search_query,


            "results":
                [],


            "error":
                str(e)

        }