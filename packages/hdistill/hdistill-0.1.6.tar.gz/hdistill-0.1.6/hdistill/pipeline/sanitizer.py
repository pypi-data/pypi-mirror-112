class Sanitizer():

    def sanitize(self, parsed_elements: []) -> []:
        """
        Removes elements that consist entirely of whitespace and strips trailing and leading whitespace

        Returns a list of sanitized elements
        """
        sanitized_elements = []
        for e in parsed_elements:
            if not e.isspace():
                sanitized_elements.append(e.strip())
        return sanitized_elements