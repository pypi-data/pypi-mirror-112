from valera import ValidationResult

__all__ = ("SubstitutionError", "make_substitution_error",)


class SubstitutionError(Exception):
    pass


def make_substitution_error(result: ValidationResult) -> SubstitutionError:
    message = ",".join(map(str, result.get_errors()))
    return SubstitutionError(message)
