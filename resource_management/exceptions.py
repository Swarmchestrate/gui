class NameMissingException(Exception):
    pass


class SatBuilderException(Exception):
    def __init__(self, message: str, problems: list[str] | None = None):
        super().__init__(message)
        # Each thing SAT Builder found wrong, for a page that lists them all
        # rather than the summary the message gives.
        self.problems = problems or []


class DescriptionMissingException(Exception):
    pass