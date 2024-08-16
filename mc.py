from langchain_cohere.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from skey import cohere_key

import os
os.environ['COHERE_API_KEY'] = cohere_key
llm = Cohere(
    temperature=0.6  # Set the temperature here
)

def generate_movie_details(genre):
    # chain 1: movie title generation
    prompt_template_title = PromptTemplate(
        input_variables=['genre'],
        template="Suggest me a movie in the {genre} genre. Suggest only one proper movie title related to this genre. Just give the one title, no explanation and don't give extra characters other than movie name."
    )

    title_chain = LLMChain(llm=llm, prompt=prompt_template_title, output_key="movie_title")

    # chain 2: plot generation
    prompt_template_plot = PromptTemplate(
        input_variables=['movie_title'],
        template="give a brief plot summary in 2 lines of the movie titled '{movie_title}'. Keep it concise, engaging, and relevant to the {genre} genre. No additional text is needed."
    )

    plot_chain = LLMChain(llm=llm, prompt=prompt_template_plot, output_key="plot")

    # chain 3: cast list generation
    prompt_template_cast = PromptTemplate(
        input_variables=['movie_title'],
        template="Give me the top five cast of the movie titled '{movie_title}'. Return the list as a comma-separated list. Just give the names, no extra characters."
    )

    cast_chain = LLMChain(llm=llm, prompt=prompt_template_cast, output_key="cast")

    chain = SequentialChain(
        chains=[title_chain, plot_chain, cast_chain],
        input_variables=['genre'],
        output_variables=['movie_title', 'plot', 'cast']
    )

    response = chain({'genre': genre})
    return response

if __name__ == "__main__":
    print(generate_movie_details("Sci-Fi"))
