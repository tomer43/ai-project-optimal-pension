from investors_types.Investor import Investor
import numpy as np


def find_best_result_arg_with_tie_breaker(results_list, max_or_min="max"):
    """
    Get the argmax in a list of results. Unlike regular numpy.argmax(), in case we have more then one maximum value
    it returns a random one
    :param results_list:    (list(float)) list of results, for example fees of different funds.
    :param max_or_min:      (str) whether to return maximum or minimum
    :return:                (int) argument of the maximum value in the list (randomly if there is more then one of them)
    """
    if max_or_min != "max" and max_or_min != "min":
        raise ValueError("max_or_min param must be either 'max' or 'min'")
    best_value = np.max(results_list) if max_or_min == "max" else np.min(results_list)
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

    def choose_fund(self, funds, quarter):
        all_funds_returns = []
        for fund in funds:
            fund_return = fund.get_fund_param(self._return_param_name, quarter)
            fund_return -= fund.get_admin_fees_by_quarter(quarter)
            all_funds_returns.append(fund_return)
        best_returns_fund_index = find_best_result_arg_with_tie_breaker(all_funds_returns, "min")
        return funds[best_returns_fund_index]


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
        super().__init__(initial_money)
        self._csv_param_name = f"sector_{sector_name}"

    def choose_fund(self, funds, quarter):
        all_funds_percentages = []
        for fund in funds:
            sector_invest_percentage = fund.get_fund_param(self._csv_param_name, quarter)
            all_funds_percentages.append(sector_invest_percentage)
        largest_sectors_fund_index = find_best_result_arg_with_tie_breaker(all_funds_percentages, "max")
        return funds[largest_sectors_fund_index]


class TechnologyInvestor(SectorialInvestor):
    def __init__(self, initial_money):
        super(TechnologyInvestor, self).__init__(initial_money, "technology")


class RealEstateInvestor(SectorialInvestor):
    def __init__(self, initial_money):
        super(RealEstateInvestor, self).__init__(initial_money, "real_estate")


class LargestFundInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, funds, quarter):
        all_funds_asset_values = []
        for fund in funds:
            fund_return = fund.get_fund_param("net_asset_value", quarter)
            all_funds_asset_values.append(fund_return)
        largest_fund_index = find_best_result_arg_with_tie_breaker(all_funds_asset_values, "max")
        return funds[largest_fund_index]


class ExpertAdviceInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, funds, quarter):
        all_funds_rating = []
        for fund in funds:
            all_funds_rating.append(fund.get_fund_param("general_rating", quarter))
        best_recommendation_fund_index = find_best_result_arg_with_tie_breaker(all_funds_rating, "max")
        return funds[best_recommendation_fund_index]


class LowestFeeInvestor(Investor):
    def __init__(self, initial_money):
        super().__init__(initial_money)

    def choose_fund(self, funds, quarter):
        fees_this_quarter = []
        for fund in funds:
            fees_this_quarter.append(fund.get_admin_fees_by_quarter(quarter))
        cheapest_fund_index = find_best_result_arg_with_tie_breaker(fees_this_quarter, "min")
        return funds[cheapest_fund_index]
