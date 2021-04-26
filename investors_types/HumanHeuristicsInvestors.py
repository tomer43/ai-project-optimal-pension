from investors_types.Investor import Investor
import numpy as np


def find_best_result_arg_with_tie_breaker(results_list, max_or_min="max"):
    """
    Get the argmax in a list of results. Unlike regular numpy.argmax(), in case we have more then one maximum value
    it returns a random one
    :param results_list:    (np.array) list of results, for example fees of different funds.
    :param max_or_min:      (str) whether to return maximum or minimum
    :return:                (int) argument of the maximum value in the list (randomly if there is more then one of them)
    """
    if max_or_min != "max" and max_or_min != "min":
        raise ValueError("max_or_min param must be either 'max' or 'min'")
    best_value = results_list.max() if max_or_min == "max" else results_list.min()
    # find all values close to maximum value in a list. np.flatnonzero returns args of close to max values.
    return np.random.choice(np.flatnonzero(np.isclose(results_list, best_value)))


class BestReturnInvestor(Investor):
    def __init__(self, initial_money, period_backward):
        super().__init__(initial_money)
        param_name_dict = {
            "quarter": "fund_last_quarter_returns",
            "year": "fund_total_last_year_returns",
            "3_years": "fund_total_last_3_years_returns",
            "5_years": "fund_total_last_5_years_returns"
        }
        self._return_param_name = param_name_dict[period_backward]

    def choose_fund(self, state):
        returns_param_idx = self._features_idx[self._return_param_name]
        expense_ratio_idx = self._features_idx['fund_quarterly_expense_ratio']
        funds_returns = state[:, returns_param_idx] - state[:, expense_ratio_idx]
        return find_best_result_arg_with_tie_breaker(funds_returns, "max")


class BestReturnLastQuarterInvestor(BestReturnInvestor):
    def __init__(self, initial_money):
        super(BestReturnLastQuarterInvestor, self).__init__(initial_money, "quarter")


class BestReturnLastYearInvestor(BestReturnInvestor):
    def __init__(self, initial_money):
        super(BestReturnLastYearInvestor, self).__init__(initial_money, "year")


class BestReturnLastThreeYearsInvestor(BestReturnInvestor):
    def __init__(self, initial_money):
        super(BestReturnLastThreeYearsInvestor, self).__init__(initial_money, "3_years")


class BestReturnLastFiveYearsInvestor(BestReturnInvestor):
    def __init__(self, initial_money):
        super(BestReturnLastFiveYearsInvestor, self).__init__(initial_money, "5_years")


class SectorialInvestor(Investor):
    def __init__(self, initial_money, sector_name):
        super(SectorialInvestor, self).__init__(initial_money)
        self._csv_param_name = f"sector_{sector_name}"

    def choose_fund(self, state):
        return find_best_result_arg_with_tie_breaker(state[:, self._features_idx[self._csv_param_name]], "max")


class TechnologyInvestor(SectorialInvestor):
    def __init__(self, initial_money):
        super(TechnologyInvestor, self).__init__(initial_money, "technology")


class RealEstateInvestor(SectorialInvestor):
    def __init__(self, initial_money):
        super(RealEstateInvestor, self).__init__(initial_money, "real_estate")


class LargestFundInvestor(Investor):
    def __init__(self, initial_money):
        super(LargestFundInvestor, self).__init__(initial_money)

    def choose_fund(self, state):
        return find_best_result_arg_with_tie_breaker(state[:, self._features_idx['net_asset_value']], "max")


class ExpertAdviceInvestor(Investor):
    def __init__(self, initial_money):
        super(ExpertAdviceInvestor, self).__init__(initial_money)

    def choose_fund(self, state):
        return find_best_result_arg_with_tie_breaker(state[:, self._features_idx['general_rating']], "max")


class LowestFeeInvestor(Investor):
    def __init__(self, initial_money):
        super(LowestFeeInvestor, self).__init__(initial_money)

    def choose_fund(self, state):
        idx = self._features_idx['fund_quarterly_expense_ratio']
        return find_best_result_arg_with_tie_breaker(state[:, idx], "min")