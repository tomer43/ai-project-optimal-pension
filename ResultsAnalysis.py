import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

sns.set(rc={'figure.figsize':(15,8)})

# working_dir = # complete path
money_cols = [f"money_q{i}" for i in range(0, 44)]

results_storage = {
    "BestReturnLastQuarter_500_experiments": {
        "name": "Last Quarter Best Return",
        "file_name": r"BestReturnLastQuarterInvestor_results 12.03.2021 16-20-53.csv"
    },

    "BestReturnLastQuarter_10k_experiments": {
        "name": "Last Quarter Best Return",
        "file_name": r"BestReturnLastQuarterInvestor_results 13.03.2021 18-00-55.csv"
    },
    "ExpertAdvice": {
        "name": "Expert Advice",
        "file_name": r"ExpertAdviceInvestor_results 17.03.2021 22-18-16.csv"
    },
    "LowestFees": {
        "name": "Lowest Fees",
        "file_name": r"LowestFeeInvestor_results 17.03.2021 21-58-30.csv"
    },
    "LargestFund": {
        "name": "Largest Fund",
        "file_name": r"LargestFundInvestor_results 17.03.2021 22-43-56.csv"
    },
    "BestReturnFiveYears": {
        "name": "Best Return over the last five years",
        "file_name": r"BestReturnLastFiveYearsInvestor_results 20.03.2021 12-49-33.csv"
    },
    "BestReturnThreeYears": {
        "name": "Best Return over the last three years",
        "file_name": r"BestReturnLastThreeYearsInvestor_results 19.03.2021 18-52-29.csv"
    },
    "BestReturnLastYear": {
        "name": "Best Return over the year",
        "file_name": r"BestReturnLastYearInvestor_results 19.03.2021 18-33-38.csv"
    },
    "BestReturnLastQuarter": {
        "name": "Best Return in the previous quarter",
        "file_name": r"BestReturnLastQuarterInvestor_results 19.03.2021 18-07-02.csv"
    },
    "RealEstate": {
        "name": "Sectorial Agent: Real Estate",
        "file_name": r"RealEstateInvestor_results 19.03.2021 17-20-28.csv"
    },
    "Technology": {
        "name": "Sectorial Agent: Technology",
        "file_name": r"TechnologyInvestor_results 19.03.2021 17-43-19.csv"
    },
    "BestInvestor": {
        "name": "Pseudo Investor: Best Case",
        "file_name": r"BestInvestor_results 19.03.2021 16-32-13.csv"
    },
    "WorstInvestor": {
        "name": "Pseudo Investor: Worst Case",
        "file_name": r"WorstInvestor_results 19.03.2021 16-54-49.csv"
    },
    "RandomInvestor": {
        "name": "Pseudo Investor: Monkey (choosing random fund)",
        "file_name": r"MonkeyInvestor_results 01.04.2021 15-19-13.csv"
    },
    "QLearningInvestor": {
        "name": "Q Learning Investor",
        "file_name": r"RLInvestor_results 25.04.2021 19-26-07.csv"
    }
}


def show_quantiles_graph(results_df, heuristic_name):
    partial_quantiles_df = results_df[money_cols].quantile(q=[0, 0.05, 0.95, 1]).transpose()
    partial_quantiles_df.rename(columns={0: "min", 1: "max", 0.05: "quantile 0.05", 0.95: "quantile 0.95"},
                                inplace=True)
    mean_df = results_df[money_cols].mean().rename("mean")
    quantiles_df = pd.concat([partial_quantiles_df, mean_df], axis=1)
    quantiles_df.rename(index={f"money_q{i}": i for i in range(0, 44)}, inplace=True)
    quantiles_df = quantiles_df[["mean", "min", "max", "quantile 0.05", "quantile 0.95"]]
    sns.lineplot(data=quantiles_df).set_title(f"Results for '{heuristic_name}' Heuristic")


def final_results_histogram(results_df, heuristic_name):
    final_res = results_df["money_q43"].rename("final_money")
    sns.histplot(final_res, stat="probability", bins=30).set_title(
        f"Distribution of Final Results for '{heuristic_name}' Heuristic")


def bleed_rates_for_heuristic(results_df, heuristic_name):
    from collections import defaultdict
    from itertools import groupby

    bleed_df = results_df.diff(1, axis=1)
    biggest_single_bleed = bleed_df.min().min()

    # calculate longest bleed
    longest_bleed = 0
    for single_experiment in bleed_df.to_numpy():
        counter = defaultdict(list)
        for key, val in groupby(single_experiment, lambda ele: "plus" if ele >= 0 else "minus"):
            counter[key].append(len(list(val)))
        curr_experiment_bleed = max(counter['minus'])
        longest_bleed = max(longest_bleed, curr_experiment_bleed)

    results_dict = {
        'biggest_bleed': biggest_single_bleed,
        'longest_bleed': longest_bleed,
    }

    return results_dict


def get_heuristic_stats(results_df, heuristic_name):
    heuristic_stats = bleed_rates_for_heuristic(results_df[money_cols], heuristic_name)
    heuristic_stats["average_gain"] = results_df["money_q43"].mean()
    heuristic_stats["maximum_gain"] = results_df["money_q43"].max()
    heuristic_stats["minimum_gain"] = results_df["money_q43"].min()
    print(f"Stats for {heuristic_name}")
    print(heuristic_stats)


def full_report_for_signel_heuristic(curr_heuristic):
    df = pd.read_csv(curr_heuristic["file_name"])
    get_heuristic_stats(df, curr_heuristic["name"])
    show_quantiles_graph(df, curr_heuristic["name"])
    plt.show()
    plt.clf()
    final_results_histogram(df, curr_heuristic["name"])
    plt.show()
    plt.clf()


if __name__ == '__main__':
    full_report_for_signel_heuristic(results_storage["QLearningInvestor"])