import sys
import re

class BracksRenderer:
    def __init__(self, template, variables=None):
        """
        Initializes the Bracks renderer with the template and optional variables.
        :param template: The Bracks template string
        :param variables: Dictionary of variables to be used in rendering the template
        """
        self.template = template
        self.variables = variables or {}

    def render(self):
        """
        Renders the Bracks template with the given variables.

        :return: The rendered template
        """
        return self._render_template()

    def _render_template(self):
        """
        Renders the Bracks template with the given variables.

        :return: The rendered template
        """
        rendered = self.template
        for key, value in self.variables.items():
            rendered = rendered.replace("[[" + key + "]]", value)

        rendered = self._process_key(rendered)
        rendered = self._process_tilde(rendered)

        return rendered

    def _extract_and_evaluate(self, template):
        """
        Extracts and evaluates Bracks expressions in the given template.

        :param template: The Bracks template string
        :return: The template with expressions evaluated
        """
        pos = 0
        while pos < len(template):
            match = re.match(r"\[\[(.*?)\]\]", template[pos:])
            if match:
                expression = match.group(1)
                evaluated = self._evaluate_expression(expression)
                template = template.replace(match.group(0), evaluated, 1)  # Replace only once
                pos += len(evaluated)
            else:
                pos += 1

        return template

    def _evaluate_expression(self, expression):
        """
        Evaluates the given Bracks expression.

        :param expression: The Bracks expression
        :return: The evaluated expression result as a string
        """
        # Handle string expressions
        if expression.startswith('str.'):
            expression = expression[4:]
            return str(eval(expression))
        elif expression == "str.center":
            sub_expression = self.extract_sub_expression(match.group(1))
            length = int(sub_expression)
            value = self.variables.get(expression[6:])
        if value is None:
            return ""
        else:
            return value.center(length)

    # Add more expression evaluation methods as needed

    def extract_sub_expression(self, expression):
        # Implement a method to extract the sub-expression inside a given expression
        pattern = r'\((.*?)\)'
        match = re.match(pattern, expression)
        if match:
            return match.group(1)
        else:
            raise ValueError("Could not extract sub-expression")

    # Implement the Key rule
    def _process_key(self, content):
        # Implement key rule processing
        pattern = r'key{{(.*?)}}'
        matches = re.findall(pattern, content)
        for match in matches:
            replacement = self.variables.get(match, '')
            content = content.replace(f'key{{{match}}}', replacement)
        return content

    # Implement the Tilde rule
    def _process_tilde(self, content):
        # Implement tilde rule processing
        pattern = r'~{{(.*?)}}'
        matches = re.findall(pattern, content)
        for match in matches:
            value = self.variables.get(match)
            if value is not None:
                approximate_value = len(value)  # For simplicity, assuming it's a string
                content = content.replace(f'~{{{match}}}', str(approximate_value))
        return content


def main():
    if len(sys.argv) < 2:
        print("Usage: python bracks3.py <template> <key1=value1> <key2=value2> ...")
        return

    template_string = sys.argv[1]
    variables = {}
    for arg in sys.argv[2:]:
        key_value_pair = arg.strip().split("=", 1)
        if len(key_value_pair) == 2:
            key, value = key_value_pair
            variables[key.strip()] = value.strip()

    bracks_renderer = BracksRenderer(template_string, variables)
    rendered_output = bracks_renderer.render()
    print(rendered_output)
    
    
if __name__ == "__main__":
    main()