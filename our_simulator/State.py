import numpy as np
from typing import Dict


def get_state_features_to_idx() -> Dict:
    """
    The list of features (columns in csv names) is how we represent a state in our simulator.
    Important Note! DO NOT edit the order of 'fund_total_last_5_years_returns' to 'fund_last_quarter_returns'
    and 'asset_stocks' to 'asset_others'. In q-learning with approximate value function, for running it with numba to
    fast things up, we assume they appear in the order in which they are now.
    """
    state_features_list = [
        'fund_total_last_5_years_returns',
        'fund_total_last_3_years_returns',
        'fund_total_last_year_returns',
        'fund_last_quarter_returns',
        'fund_quarterly_expense_ratio',
        'asset_stocks',
        'asset_bonds',
        'asset_cash',
        'asset_others',
        'inception_date',
        'general_rating',
        'return_rating',
        'risk_rating',
        'net_asset_value',
        'median_market_cap',
        'sector_technology',
        'sector_real_estate',

        # When running pseudo-agents, we also need to have 'fund_returns' as part of the state.
        # this is in comment to prevent data leakage
        # 'fund_returns',
    ]
    features_to_idx = {item: idx for idx, item in enumerate(state_features_list)}
    return features_to_idx


def get_funds_param_by_quarter(funds, param_name, quarter_idx):
    if quarter_idx == 43:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    else:
        funds_params_by_quarter = [0] * 10
        for i, fund in enumerate(funds):
            funds_params_by_quarter[i] = fund.get_fund_param(param_name, quarter_idx)
        return tuple(funds_params_by_quarter)


def get_state(funds, turn):
    params_to_use = get_state_features_to_idx()
    state_parameters = np.ndarray((10, len(params_to_use.keys())))
    for param in params_to_use.keys():
        state_parameters[:, params_to_use[param]] = get_funds_param_by_quarter(funds, param, turn)
    return state_parameters
