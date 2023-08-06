# Copyright PA Knowledge Ltd 2021

from mergedeep import merge, Strategy


class JoinSisl:

    @classmethod
    def join(cls, list_of_dicts):
        return merge({}, *list_of_dicts, strategy=Strategy.TYPESAFE_ADDITIVE)
