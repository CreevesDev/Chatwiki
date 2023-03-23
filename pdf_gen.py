import jinja2
import os

"""
Sets Jinja2 environment, using syntax that won't clash with LaTeX syntax.
Be careful if following examples online etc. which will use different syntax.
"""
latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader =
jinja2.FileSystemLoader(os.path.abspath('.'))
)

def generate_pdf(concept):
    """
    Generates a PDF using pdflatex, with the tex file formatted using Jinja2. 
    :param concept: The concept object created in main.py
    """
    template = latex_jinja_env.get_template('template.tex')
    print(concept.topics_and_answers)
    
	#Defining the variables to be substituted into the template. 
    variables = {
        'protein_name': concept.title,
        'openai_summary': concept.openai_summary,
        'topics_and_answers': concept.topics_and_answers,
        'papers': concept.papers
    }
    rendered = template.render(variables)
    with open('output/output.tex', 'w') as f:
        f.write(rendered)
    os.system('pdflatex -output-directory=output output/output.tex'.format(concept.title_formatted)) # > /dev/null 2>&1
    os.rename('output/output.pdf', "output/"+concept.title_formatted+".pdf")