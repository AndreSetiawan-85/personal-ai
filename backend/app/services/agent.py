from app.tools import TOOLS

from app.services.ollama import (
    ollama_service
)

from app.services.search_router import (
    detect_search_type
)

from app.services.citation import (
    format_citations
)



class AgentService:


    def __init__(self):

        self.tools = TOOLS



    def detect_tool(
        self,
        message: str
    ):


        text = message.lower()



        # =====================
        # Calculator Detection
        # =====================


        math_keywords = [

            "+",
            "-",
            "*",
            "/",
            "berapa",
            "hitung",
            "kali",
            "tambah",
            "kurang",
            "bagi",

        ]


        if any(
            keyword in text
            for keyword in math_keywords
        ):

            return "calculator"




        # =====================
        # Web Search Detection
        # =====================


        domain = detect_search_type(
            message
        )


        search_domains = [

            "news",
            "food",
            "travel",
            "shopping",
            "coding",
            "finance",
            "health",
            "entertainment",

        ]



        if domain in search_domains:

            return "web_search"



        return None






    def run(
        self,
        message: str
    ):


        tool_name = self.detect_tool(
            message
        )



        domain = None

        result = None

        citations = []




        # =====================
        # Normal Chat
        # =====================


        if not tool_name:


            return ollama_service.generate_response(

                message

            )





        tool = self.tools.get(
            tool_name
        )



        if not tool:


            return ollama_service.generate_response(

                message

            )






        # =====================
        # Calculator
        # =====================


        if tool_name == "calculator":



            expression = (

                message

                .lower()

                .replace(
                    "berapa",
                    ""
                )

                .replace(
                    "hitung",
                    ""
                )

                .replace(
                    "hasil",
                    ""
                )

                .replace(
                    "adalah",
                    ""
                )

                .strip()

            )



            result = tool(
                expression
            )





        # =====================
        # Web Search
        # =====================


        elif tool_name == "web_search":



            domain = detect_search_type(
                message
            )



            result = tool(
                message
            )



            citations = format_citations(

                result.get(
                    "results",
                    []
                )

            )







        # =====================
        # Generate Answer
        # =====================


        prompt = f"""

Kamu adalah Gwen,
AI assistant pribadi.


Pertanyaan user:

{message}



Kategori:

{domain}



Data dari tool:

{result}



Sumber:

{citations}



Aturan menjawab:

1. Jawab menggunakan bahasa natural.
2. Jangan menyebut proses internal.
3. Jangan membuat sumber palsu.
4. Jika ada sumber, tampilkan sumber.
5. Jika informasi kurang yakin, katakan bahwa informasi perlu diverifikasi.
6. Untuk berita gunakan format ringkas.



"""


        return ollama_service.generate_response(

            prompt

        )





agent_service = AgentService()