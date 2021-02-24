class Fund:
    def __init__(self, fund_details):
        self.fund_symbol = fund_details[0]
        self.ts = fund_details[1]
        self.fund_family = fund_details[2]
        self.inception_date = fund_details[3]
        self.category = fund_details[4]
        self.general_rating = fund_details[5]
        self.return_rating = fund_details[6]
        self.risk_rating = fund_details[7]
        self.net_asset_value = fund_details[8]
        self.median_market_cap = fund_details[9]
        self.fund_returns = fund_details[10]  # returns
        self.fund_last_quarter_returns = fund_details[11]
        self.fund_total_last_year_returns = fund_details[12]
        self.fund_total_last_3_years_returns = fund_details[13]
        self.fund_total_last_5_years_returns = fund_details[14]
        self.category_returns = fund_details[15]
        self.category_last_quarter_returns = fund_details[16]
        self.category_total_last_year_returns = fund_details[17]
        self.category_total_last_3_years_returns = fund_details[18]
        self.category_total_last_5_years_returns = fund_details[19]
        self.fund_quarterly_expense_ratio = fund_details[20]  # administration fees
        self.fund_quarterly_expense_ratio_previous_quarter = fund_details[21]
        self.fund_quarterly_expense_ratio_average_previous_year = fund_details[22]
        self.fund_quarterly_expense_ratio_average_previous_two_years = fund_details[23]
        self.category_quarterly_expense_ratio = fund_details[24]
        self.category_quarterly_expense_ratio_previous_quarter = fund_details[25]
        self.category_quarterly_expense_ratio_average_previous_year = fund_details[26]
        self.category_quarterly_expense_ratio_average_previous_two_years = fund_details[27]
        self.sector_communication_services = fund_details[28]
        self.sector_consumer_defensive = fund_details[29]
        self.sector_healthcare = fund_details[30]
        self.sector_utilities = fund_details[31]
        self.sector_consumer_cyclical = fund_details[32]
        self.sector_energy = fund_details[33]
        self.sector_others = fund_details[34]
        self.sector_industrials = fund_details[35]
        self.sector_financial_services = fund_details[36]
        self.sector_technology = fund_details[37]
        self.sector_basic_materials = fund_details[38]
        self.sector_real_estate = fund_details[39]
        self.asset_cash = fund_details[40]
        self.asset_stocks = fund_details[41]
        self.asset_bonds = fund_details[42]
        self.asset_others = fund_details[43]
        self.asset_preferred = fund_details[44]
        self.asset_convertable = fund_details[45]
        self.price_earnings_ratio = fund_details[46]
        self.price_book_ratio = fund_details[47]
        self.price_sales_ratio = fund_details[48]
        self.price_cashflow_ratio = fund_details[49]

    def getSymbol(self):
        return self.fund_symbol

    def getAdminFees(self):
        # return self.fund_net_annual_expense_ratio
        return self.fund_quarterly_expense_ratio

    def getReturns(self):
        return self.fund_returns

    def __str__(self):
        # fund_str = 'Fund symbol: ' + self.fund_symbol + '\n'
        # fund_str += '\t' + 'Administration fees:\t' + str(self.getAdminFees()) + '\n'
        # fund_str += '\t' + 'Returns:\t\t\t\t' + str(self.getReturns()) + '\n'

        fund_str = 'Fund symbol: ' + self.fund_symbol + '\n'
        fund_str += '\t' + 'ts:\t' + str(self.ts) + '\n'
        fund_str += '\t' + 'fund_family:\t' + str(self.fund_family) + '\n'
        fund_str += '\t' + 'inception_date:\t' + str(self.inception_date) + '\n'
        fund_str += '\t' + 'category:\t' + str(self.category) + '\n'
        fund_str += '\t' + 'general_rating:\t' + str(self.general_rating) + '\n'
        fund_str += '\t' + 'return_rating:\t' + str(self.return_rating) + '\n'
        fund_str += '\t' + 'risk_rating:\t' + str(self.risk_rating) + '\n'
        fund_str += '\t' + 'net_asset_value:\t' + str(self.net_asset_value) + '\n'
        fund_str += '\t' + 'median_market_cap:\t' + str(self.median_market_cap) + '\n'
        fund_str += '\t' + 'fund_returns:\t' + str(self.fund_returns) + '\n'
        fund_str += '\t' + 'fund_last_quarter_returns:\t' + str(self.fund_last_quarter_returns) + '\n'
        fund_str += '\t' + 'fund_total_last_year_returns:\t' + str(self.fund_total_last_year_returns) + '\n'
        fund_str += '\t' + 'fund_total_last_3_years_returns:\t' + str(self.fund_total_last_3_years_returns) + '\n'
        fund_str += '\t' + 'fund_total_last_5_years_returns:\t' + str(self.fund_total_last_5_years_returns) + '\n'
        fund_str += '\t' + 'category_returns:\t' + str(self.category_returns) + '\n'
        fund_str += '\t' + 'category_last_quarter_returns:\t' + str(self.category_last_quarter_returns) + '\n'
        fund_str += '\t' + 'category_total_last_year_returns:\t' + str(self.category_total_last_year_returns) + '\n'
        fund_str += '\t' + 'category_total_last_3_years_returns:\t' + str(self.category_total_last_3_years_returns) + '\n'
        fund_str += '\t' + 'category_total_last_5_years_returns:\t' + str(self.category_total_last_5_years_returns) + '\n'
        fund_str += '\t' + 'fund_quarterly_expense_ratio:\t' + str(self.fund_quarterly_expense_ratio) + '\n'
        fund_str += '\t' + 'fund_quarterly_expense_ratio_previous_quarter:\t' + str(self.fund_quarterly_expense_ratio_previous_quarter) + '\n'
        fund_str += '\t' + 'fund_quarterly_expense_ratio_average_previous_year:\t' + str(self.fund_quarterly_expense_ratio_average_previous_year) + '\n'
        fund_str += '\t' + 'fund_quarterly_expense_ratio_average_previous_two_years:\t' + str(self.fund_quarterly_expense_ratio_average_previous_two_years) + '\n'
        fund_str += '\t' + 'category_quarterly_expense_ratio:\t' + str(self.category_quarterly_expense_ratio) + '\n'
        fund_str += '\t' + 'category_quarterly_expense_ratio_previous_quarter:\t' + str(self.category_quarterly_expense_ratio_previous_quarter) + '\n'
        fund_str += '\t' + 'category_quarterly_expense_ratio_average_previous_year:\t' + str(self.category_quarterly_expense_ratio_average_previous_year) + '\n'
        fund_str += '\t' + 'category_quarterly_expense_ratio_average_previous_two_years:\t' + str(self.category_quarterly_expense_ratio_average_previous_two_years) + '\n'
        fund_str += '\t' + 'sector_communication_services:\t' + str(self.sector_communication_services) + '\n'
        fund_str += '\t' + 'sector_consumer_defensive:\t' + str(self.sector_consumer_defensive) + '\n'
        fund_str += '\t' + 'sector_healthcare:\t' + str(self.sector_healthcare) + '\n'
        fund_str += '\t' + 'sector_utilities:\t' + str(self.sector_utilities) + '\n'
        fund_str += '\t' + 'sector_consumer_cyclical:\t' + str(self.sector_consumer_cyclical) + '\n'
        fund_str += '\t' + 'sector_energy:\t' + str(self.sector_energy) + '\n'
        fund_str += '\t' + 'sector_others:\t' + str(self.sector_others) + '\n'
        fund_str += '\t' + 'sector_industrials:\t' + str(self.sector_industrials) + '\n'
        fund_str += '\t' + 'sector_financial_services:\t' + str(self.sector_financial_services) + '\n'
        fund_str += '\t' + 'sector_technology:\t' + str(self.sector_technology) + '\n'
        fund_str += '\t' + 'sector_basic_materials:\t' + str(self.sector_basic_materials) + '\n'
        fund_str += '\t' + 'sector_real_estate:\t' + str(self.sector_real_estate) + '\n'
        fund_str += '\t' + 'asset_cash:\t' + str(self.asset_cash) + '\n'
        fund_str += '\t' + 'asset_stocks:\t' + str(self.asset_stocks) + '\n'
        fund_str += '\t' + 'asset_bonds:\t' + str(self.asset_bonds) + '\n'
        fund_str += '\t' + 'asset_others:\t' + str(self.asset_others) + '\n'
        fund_str += '\t' + 'asset_preferred:\t' + str(self.asset_preferred) + '\n'
        fund_str += '\t' + 'asset_convertable:\t' + str(self.asset_convertable) + '\n'
        fund_str += '\t' + 'price_earnings_ratio:\t' + str(self.price_earnings_ratio) + '\n'
        fund_str += '\t' + 'price_book_ratio:\t' + str(self.price_book_ratio) + '\n'
        fund_str += '\t' + 'price_sales_ratio:\t' + str(self.price_sales_ratio) + '\n'
        fund_str += '\t' + 'price_cashflow_ratio:\t' + str(self.price_cashflow_ratio) + '\n'

        fund_str += '\n'
        return fund_str
