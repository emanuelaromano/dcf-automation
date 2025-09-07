import numpy as np
import pandas as pd
import openturns as ot
from plotly.io import to_html
import scipy.stats

########################################################
# DATA FRAME FLATTENER
########################################################

def data_frame_flattener(df):
    """
    Collapse a multi‐level column index into single strings.
    E.g. columns [(‘A’,‘x’),(‘B’,‘y’)] → [‘A x’, ‘B y’].
    """
    df = df.copy()
    if hasattr(df.columns, "levels") and df.columns.nlevels > 1:
        df.columns = [
            " ".join(map(str, col)).strip() 
            for col in df.columns.values
        ]
    return df


########################################################
# COLUMN SUFFIX ADDER
########################################################


def column_suffix_adder(df, cols, suffix):
    """
    Add `suffix` to the names of columns in `cols`.
    E.g. col='value', suffix='_new' → 'value_new'.
    """
    df = df.copy()
    # Build a rename map only for the requested columns
    rename_map = {col: f"{col}{suffix}" for col in cols if col in df.columns}
    df = df.rename(columns=rename_map)
    return df

########################################################
# DYNAMIC CONVERGER
########################################################

def dynamic_converger(current,
                      expected,
                      number_of_steps,
                      period_to_begin_to_converge):
    """This Function is to project growth in 2 phase.
    Phase 1: You grow  Period after period for number of period specified.
    Phase 2: growth begin to converge to number_of_steps value.
    current: beginning growth_rate
    expected: final growth rate
    period_to_begin_to_converge: Period to begin to transition to terminal growth value
    number_of_steps: number of period (years) to project growth."""
    number_of_steps =  int(number_of_steps)
    period_to_begin_to_converge = int(period_to_begin_to_converge)
    def converger(current,
                expected,
                number_of_steps):
        values = np.linspace(current,expected,number_of_steps+1)
        return(values)

    array_phase1 = np.array([current]*(period_to_begin_to_converge-1))

    array_phase2 = converger(current,
                       expected,
                       number_of_steps-period_to_begin_to_converge)
    result= pd.Series(np.concatenate((array_phase1,array_phase2)))
    return(result)


########################################################
# DYNAMIC CONVERGER MULTIPLE PHASE
########################################################

def dynamic_converger_multiple_phase(growth_rates_for_each_cylce,
                                     length_of_each_cylce,
                                     convergance_periods):
    list_of_results = []
    for cycle in range(len(length_of_each_cylce)):
        result = dynamic_converger(current = growth_rates_for_each_cylce[cycle][0],
                        expected = growth_rates_for_each_cylce[cycle][1],
                        number_of_steps = length_of_each_cylce[cycle],
                        period_to_begin_to_converge = convergance_periods[cycle])
        list_of_results.append(result)
    return(pd.concat(list_of_results,ignore_index=True))


########################################################
# REVENUE PROJECTOR MULTIPLE PHASE
########################################################

def revenue_projector_multi_phase(revenue_base,
                                  revenue_growth_rate_cycle1_begin,
                                  revenue_growth_rate_cycle1_end,
                                  revenue_growth_rate_cycle2_begin,
                                  revenue_growth_rate_cycle2_end,
                                  revenue_growth_rate_cycle3_begin,
                                  revenue_growth_rate_cycle3_end = 0.028,
                                  length_of_cycle1=3,
                                  length_of_cycle2=4,
                                  length_of_cycle3=3,
                                  revenue_convergance_periods_cycle1 =1,
                                  revenue_convergance_periods_cycle2=1,
                                  revenue_convergance_periods_cycle3=1):
    projected_revenue_growth = dynamic_converger_multiple_phase(growth_rates_for_each_cylce= [[revenue_growth_rate_cycle1_begin,revenue_growth_rate_cycle1_end],
                                                               [revenue_growth_rate_cycle2_begin,revenue_growth_rate_cycle2_end],
                                                               [revenue_growth_rate_cycle3_begin,revenue_growth_rate_cycle3_end]],
                                     length_of_each_cylce=[length_of_cycle1,length_of_cycle2,length_of_cycle3],
                                     convergance_periods=[revenue_convergance_periods_cycle1,
                                                          revenue_convergance_periods_cycle2,
                                                          revenue_convergance_periods_cycle3])
    ### Compute Cumulative revenue_growth
    projected_revenue_growth_cumulative = (1+projected_revenue_growth).cumprod()
    projected_revenues = revenue_base*projected_revenue_growth_cumulative
    return(projected_revenues,projected_revenue_growth)


########################################################
# OPERATING MARGIN PROJECTOR
########################################################    

def operating_margin_projector(current_operating_margin,
                               terminal_operating_margin,
                               valuation_interval_in_years=10,
                               year_operating_margin_begins_to_converge_to_terminal_operating_margin=5):
    projectd_operating_margin = dynamic_converger(current_operating_margin,
                                                  terminal_operating_margin,
                                                  valuation_interval_in_years,
                                                  year_operating_margin_begins_to_converge_to_terminal_operating_margin)
    return(projectd_operating_margin)


########################################################
# TAX RATE PROJECTOR
########################################################

def tax_rate_projector(current_effective_tax_rate,
                      marginal_tax_rate,
                      valuation_interval_in_years=10,
                      year_effective_tax_rate_begin_to_converge_marginal_tax_rate=5):
    """Project tax rate during valuation Cylce"""
    projected_tax_rate = dynamic_converger(current_effective_tax_rate,
                                           marginal_tax_rate,
                                           valuation_interval_in_years,
                                           year_effective_tax_rate_begin_to_converge_marginal_tax_rate)
    return(projected_tax_rate)



########################################################
# COST OF CAPITAL PROJECTOR
########################################################

def cost_of_capital_projector(unlevered_beta,
                              terminal_unlevered_beta,
                              current_pretax_cost_of_debt,
                              terminal_pretax_cost_of_debt,
                              equity_value,
                              debt_value,
                              marginal_tax_rate=.21,
                              risk_free_rate=0.015,
                              ERP=0.055,
                              valuation_interval_in_years=10,
                              year_beta_begins_to_converge_to_terminal_beta=5,
                              year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt=5):
    """Project Cost of Capiatal during valuation Cylce"""
    ### Compute Beta During Valuatio Cycle
    ### Company Levered Beta  = Unlevered beta * (1 + (1- tax rate) (Debt/Equity))
    company_beta = unlevered_beta * (1+(1-marginal_tax_rate)*(debt_value/equity_value))
    terminal_beta = terminal_unlevered_beta * (1+(1-marginal_tax_rate)*(debt_value/equity_value))
    beta_druing_valution_cycle = dynamic_converger(company_beta,
                                                   terminal_beta,
                                                   valuation_interval_in_years,
                                                   year_beta_begins_to_converge_to_terminal_beta)
    ### Compute Pre Tax Cost Of debt During Valuation Cycle
    pre_tax_cost_of_debt_during_valution_cycle = dynamic_converger(current_pretax_cost_of_debt,
                                                                   terminal_pretax_cost_of_debt,
                                                                   valuation_interval_in_years,
                                                                   year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt)

    total_capital = equity_value+debt_value
    equity_to_capital = equity_value/total_capital
    debt_to_capital = debt_value/total_capital
    after_tax_cost_of_debt_during_valution_cycle = pre_tax_cost_of_debt_during_valution_cycle*(1-marginal_tax_rate)
    cost_of_equity = risk_free_rate + (beta_druing_valution_cycle*ERP)
    cost_of_capital_during_valuatio_cycle = ((equity_to_capital*cost_of_equity)+
                                             (debt_to_capital*after_tax_cost_of_debt_during_valution_cycle))
    return(cost_of_capital_during_valuatio_cycle,beta_druing_valution_cycle,terminal_beta,cost_of_equity,after_tax_cost_of_debt_during_valution_cycle)


########################################################
# REVENUE PROJECTOR
########################################################

def revenue_growth_projector(revenue_growth_rate,
                             terminal_growth_rate=.028,
                             valuation_interval_in_years=10,
                             year_revenue_growth_begin_to_converge_to_terminal_growth_rate = 5):
    """Project revenue growth during valuation Cylce"""
    projected_revenue_growth = dynamic_converger(revenue_growth_rate,
                                                 terminal_growth_rate,
                                                 valuation_interval_in_years,
                                                 year_revenue_growth_begin_to_converge_to_terminal_growth_rate)
    return(projected_revenue_growth)


########################################################
# REVENUE PROJECTOR
########################################################

def revenue_projector(revenue_base,
                      revenue_growth_rate,
                      terminal_growth_rate,
                      valuation_interval_in_years,
                      year_revenue_growth_begin_to_converge_to_terminal_growth_rate):
    ### Estimate Revenue Growth
    projected_revenue_growth = revenue_growth_projector(revenue_growth_rate=revenue_growth_rate,
                                                        terminal_growth_rate = terminal_growth_rate,
                                                        valuation_interval_in_years=valuation_interval_in_years,
                                                        year_revenue_growth_begin_to_converge_to_terminal_growth_rate=year_revenue_growth_begin_to_converge_to_terminal_growth_rate)
    ### Compute Cummulative revenue_growth
    projected_revenue_growth_cumulative = (1+projected_revenue_growth).cumprod()
    projected_revenues = revenue_base*projected_revenue_growth_cumulative
    return(projected_revenues,projected_revenue_growth)


########################################################
# SALES TO CAPITAL PROJECTOR
########################################################

def sales_to_capital_projector(current_sales_to_capital_ratio,
                               terminal_sales_to_capital_ratio,
                               valuation_interval_in_years=10,
                               year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital=3):
    projectd_sales_to_capital = dynamic_converger(current_sales_to_capital_ratio,
                                                  terminal_sales_to_capital_ratio,
                                                  valuation_interval_in_years,
                                                  year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital)
    return(projectd_sales_to_capital)


########################################################
# REINVESTMENT PROJECTOR
########################################################

def reinvestment_projector(revenue_base,
                           projected_revenues,
                           sales_to_capital_ratios,
                           asset_liquidation_during_negative_growth=0):
    reinvestment = (pd.concat([pd.Series(revenue_base),
                               projected_revenues],
                             ignore_index=False).diff().dropna()/sales_to_capital_ratios)
    reinvestment = reinvestment.where(reinvestment>0, (reinvestment*asset_liquidation_during_negative_growth))
    return(reinvestment)


########################################################
# VALUATOR MULTI PHASE
########################################################

def valuator_multi_phase(
    risk_free_rate,
    ERP,
    equity_value,
    debt_value,
    unlevered_beta,
    terminal_unlevered_beta,
    year_beta_begins_to_converge_to_terminal_beta,
    current_pretax_cost_of_debt,
    terminal_pretax_cost_of_debt,
    year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt,
    current_effective_tax_rate,
    marginal_tax_rate,
    year_effective_tax_rate_begin_to_converge_marginal_tax_rate,
    revenue_base,
    revenue_growth_rate_cycle1_begin,
    revenue_growth_rate_cycle1_end,
    revenue_growth_rate_cycle2_begin,
    revenue_growth_rate_cycle2_end,
    revenue_growth_rate_cycle3_begin,
    revenue_growth_rate_cycle3_end,
    revenue_convergance_periods_cycle1,
    revenue_convergance_periods_cycle2,
    revenue_convergance_periods_cycle3,
    length_of_cycle1,
    length_of_cycle2,
    length_of_cycle3,
    current_sales_to_capital_ratio,
    terminal_sales_to_capital_ratio,
    year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital,
    current_operating_margin,
    terminal_operating_margin,
    year_operating_margin_begins_to_converge_to_terminal_operating_margin,
    additional_return_on_cost_of_capital_in_perpetuity=0.0,
    cash_and_non_operating_asset=0.0,
    asset_liquidation_during_negative_growth=0,
    current_invested_capital='implicit'):
    """
    Value business with 3 cycles

    Parameters
    ----------
    risk_free_rate : riks free rate in the dominated currency you perform the D.C.F - if USD, then 10 year T Bond is a decent proxy

    ERP: Equity Risk Premium - How much investors are expecting to earn on stocks in excess of holidng risk free assest such as treasuries,

    equity_value: Estimate Equity value of the business. This is used to estimate Weighted Average Cost of Capital aka WACC,

    debt_value: Market value or Book value of debt in the business,

    unlevered_beta : current unlevered beta (beta adjusted for debt - leverage) of the industry

    terminal_unlevered_beta: terminal unlevered beta (beta adjusted for debt - leverage) of the industry
    if valuing a frim in new space such as AI or Metaverse, intuitively you should have high beta (high risk profile) today, but in 10 years the beta should decrease as the space is more known and business matures

    year_beta_begins_to_converge_to_terminal_beta: The year which the convergence between unlevered_beta and terminal_unlevered_beta will begin to materialize

    current_pretax_cost_of_debt : Cost of rasing fresh debt - pre tax (the model takes interst expense deduction into account)

    terminal_pretax_cost_of_debt : Cost of rasing fresh debt - pre tax (the model takes interst expense deduction into account) at maturity

    year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt : The year which the convergence between current_pretax_cost_of_debt  and terminal_pretax_cost_of_debt will begin to materialize

    current_effective_tax_rate : Effecive tax rate, can be found on the income statement

    marginal_tax_rate : Marginal Tax rate of your company - for mature companies effective tax rate should be close or equal to marginal_tax_rate

    year_effective_tax_rate_begin_to_converge_marginal_tax_rate : The year which the convergence between current_effective_tax_rate and marginal_tax_rate will begin to materialize

    revenue_base: Current TTM revenue or normalized revenue - whatever you think is appropriate as your base revenue

    revenue_growth_rate_cycle1_begin : revenue growth rate at the begining of the 1st cycle

    revenue_growth_rate_cycle1_end : revenue growth rate at the end of the 1st cycle

    revenue_growth_rate_cycle2_begin : revenue growth rate at the begining of the 2nd cycle

    revenue_growth_rate_cycle2_end : revenue growth rate at the end of the 1st cycle

    revenue_growth_rate_cycle3_begin : revenue growth rate at the begining of the 3rd cycle

    revenue_growth_rate_cycle3_end : revenue growth rate at the end of the 3rd cycle - aka Terminal growth rate - should not exceed your risk free rate

    revenue_convergance_periods_cycle1 : The year which the convergence between revenue_growth_rate_cycle1_begin and revenue_growth_rate_cycle1_end will begin to materialize

    revenue_convergance_periods_cycle2 : The year which the convergence between revenue_growth_rate_cycle2_begin and revenue_growth_rate_cycle2_end will begin to materialize

    revenue_convergance_periods_cycle3 : The year which the convergence between revenue_growth_rate_cycle3_begin and revenue_growth_rate_cycle3_end will begin to materialize

    length_of_cycle1 : number of years that cycle 1 will last

    length_of_cycle2 : number of years that cycle 2 will last

    length_of_cycle3 : number of years that cycle 3 will last

    current_sales_to_capital_ratio : estimated reinvestment based upon the change in revenues and the sales to capital ratio
    Reinvestmentt = Change in revenuest/ (Sales/Capital)
    assuming a sales to capital ratio of 2.5, in conjunction with a revenue increase of $ 250 million will result in reinvestment of $ 100 million

    terminal_sales_to_capital_ratio : terminal sales to capital ratio

    year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital : The year which the convergence between current_sales_to_capital_ratio and terminal_sales_to_capital_ratio will begin to materialize

    current_operating_margin : TTM to normalized ebit margin (operating margin)

    terminal_operating_margin : Terminal operating margin - should be close to industry average - might possibly be higher or lower than industry average if your company has demostrate lower or higher than average quality in earning and reinvetment etc.

    year_operating_margin_begins_to_converge_to_terminal_operating_margin: The year which the convergence between current_operating_margin and terminal_operating_margin will begin to materialize

    additional_return_on_cost_of_capital_in_perpetuity: Reinvestment rate in mature phase is required to keep the operating going - if your firm is able to earn higher than their cost of capital - which is rare -
    enter your estimated  excess return on capital in perpetuity

    cash_and_non_operating_asset : non operating investment as cash, such as holding in other companies, treasuries etc,

    asset_liquidation_during_negative_growth: If your bussines is declining as you are selling assets, how many % relative to your sales to capital ration you earn

    current_invested_capital : current value of deployed capital (asset in place) should include tangible and intangible

    """
    valuation_interval_in_years = int(length_of_cycle1) + int(length_of_cycle2) + int(length_of_cycle3)
    terminal_growth_rate = revenue_growth_rate_cycle3_end
    ### Estimate Cost of Capital during the valution cycle
    projected_cost_of_capital, projected_beta , terminal_beta , projected_cost_of_equity , projected_after_tax_cost_of_debt = cost_of_capital_projector(unlevered_beta=unlevered_beta,
                                                          terminal_unlevered_beta=terminal_unlevered_beta,
                                                          current_pretax_cost_of_debt=current_pretax_cost_of_debt,
                                                          terminal_pretax_cost_of_debt=terminal_pretax_cost_of_debt,
                                                          equity_value=equity_value,
                                                          debt_value=debt_value,
                                                          marginal_tax_rate=marginal_tax_rate,
                                                          risk_free_rate=risk_free_rate,
                                                          ERP=ERP,
                                                          valuation_interval_in_years=valuation_interval_in_years,
                                                          year_beta_begins_to_converge_to_terminal_beta=year_beta_begins_to_converge_to_terminal_beta,
                                                          year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt=year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt)
    projected_cost_of_capital_cumulative= (1+projected_cost_of_capital).cumprod()
    projected_cost_of_equity_cumulative= (1+projected_cost_of_equity).cumprod()
    ### Estimate Future revnues, and growth

    projected_revenues,projected_revenue_growth = revenue_projector_multi_phase(revenue_base = revenue_base,
                                  revenue_growth_rate_cycle1_begin = revenue_growth_rate_cycle1_begin,
                                  revenue_growth_rate_cycle1_end = revenue_growth_rate_cycle1_end,
                                  revenue_growth_rate_cycle2_begin = revenue_growth_rate_cycle2_begin,
                                  revenue_growth_rate_cycle2_end = revenue_growth_rate_cycle2_end,
                                  revenue_growth_rate_cycle3_begin = revenue_growth_rate_cycle3_begin,
                                  revenue_growth_rate_cycle3_end = revenue_growth_rate_cycle3_end,
                                  length_of_cycle1=length_of_cycle1,
                                  length_of_cycle2=length_of_cycle2,
                                  length_of_cycle3=length_of_cycle3,
                                  revenue_convergance_periods_cycle1 = revenue_convergance_periods_cycle1,
                                  revenue_convergance_periods_cycle2 = revenue_convergance_periods_cycle2,
                                  revenue_convergance_periods_cycle3 = revenue_convergance_periods_cycle3)
    ### Estmimate tax rates
    projected_tax_rates = tax_rate_projector(current_effective_tax_rate=current_effective_tax_rate,
                                            marginal_tax_rate=marginal_tax_rate,
                                            valuation_interval_in_years=valuation_interval_in_years,
                                            year_effective_tax_rate_begin_to_converge_marginal_tax_rate=year_effective_tax_rate_begin_to_converge_marginal_tax_rate)
    ### Estimate slaes to capital ratio during valuation for reinvestment
    sales_to_capital_ratios = sales_to_capital_projector(current_sales_to_capital_ratio,
                               terminal_sales_to_capital_ratio,
                               valuation_interval_in_years=valuation_interval_in_years,
                               year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital=year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital)

    ### Estimate Reinvestemnt
    projected_reinvestment = reinvestment_projector(revenue_base=revenue_base,
                                                    projected_revenues = projected_revenues,
                                                    sales_to_capital_ratios=sales_to_capital_ratios,
                                                    asset_liquidation_during_negative_growth=asset_liquidation_during_negative_growth)

    ### Estimate invested Capital
    invested_capital = projected_reinvestment.copy()
    if current_invested_capital == 'implicit':
        current_invested_capital = revenue_base / current_sales_to_capital_ratio
    invested_capital[0] = invested_capital[0] + current_invested_capital
    invested_capital = invested_capital.cumsum()

    ### Operating Margin
    projected_operating_margins = operating_margin_projector(current_operating_margin,
                                                            terminal_operating_margin,
                                                            valuation_interval_in_years=valuation_interval_in_years,
                                                            year_operating_margin_begins_to_converge_to_terminal_operating_margin=year_operating_margin_begins_to_converge_to_terminal_operating_margin)
    ###EBIT
    projected_operating_income = projected_revenues * projected_operating_margins
    ### After Tax EBIT (EBI)
    projected_operating_income_after_tax = (projected_operating_income*(1-projected_tax_rates))
    ### FCFF: EBI-Reinvestment
    projected_FCFF = projected_operating_income_after_tax - projected_reinvestment
    ### compute ROIC
    ROIC = (projected_operating_income_after_tax/invested_capital)
    ### Compute Terminal Value
    terminal_cost_of_capital = projected_cost_of_capital[-1:].values
    terminal_cost_of_equity = projected_cost_of_equity[-1:].values
    if terminal_growth_rate < 0:
        terminal_reinvestment_rate=0
    else:
        terminal_reinvestment_rate = terminal_growth_rate/(terminal_cost_of_capital+additional_return_on_cost_of_capital_in_perpetuity)
    terminal_revenue = projected_revenues[-1:].values * (1+terminal_growth_rate)
    terminal_operating_income = terminal_revenue * terminal_operating_margin
    terminal_operating_income_after_tax = terminal_operating_income*(1-marginal_tax_rate)
    terminal_reinvestment = terminal_operating_income_after_tax* terminal_reinvestment_rate
    terminal_FCFF = terminal_operating_income_after_tax - terminal_reinvestment
    terminal_value = terminal_FCFF/(terminal_cost_of_capital-terminal_growth_rate)
    termimal_discount_rate = (terminal_cost_of_capital-terminal_growth_rate)*(1+projected_cost_of_capital).prod()
    termimal_equity_discount_rate = (terminal_cost_of_equity-terminal_growth_rate)*(1+projected_cost_of_equity).prod()


    ### Concatinate Projected Values with termianl values
    projected_cost_of_capital_cumulative_with_terminal_rate =pd.concat([projected_cost_of_capital_cumulative,
                                                    pd.Series(termimal_discount_rate)])
    projected_cost_of_equity_cumulative_with_terminal_rate = pd.concat([projected_cost_of_equity_cumulative,
                                                    pd.Series(termimal_equity_discount_rate)])

    projected_revenue_growth = pd.concat([projected_revenue_growth,
                                        pd.Series(terminal_growth_rate)])
    projected_revenues =pd.concat([projected_revenues,
                                  pd.Series(terminal_revenue)])
    projected_tax_rates = pd.concat([projected_tax_rates,
                                   pd.Series(marginal_tax_rate)])
    projected_reinvestment = pd.concat([projected_reinvestment,
                                        pd.Series(terminal_reinvestment)])


    ### Estimate invested Capital
    invested_capital = pd.concat([invested_capital,
                                        pd.Series(np.nan)])
    ### Estimate ROIC
    terminal_ROIC = terminal_cost_of_capital+additional_return_on_cost_of_capital_in_perpetuity
    ROIC = pd.concat([ROIC,
                      pd.Series(terminal_ROIC)])

    projected_operating_margins = pd.concat([projected_operating_margins,
                                        pd.Series(terminal_operating_margin)])
    projected_operating_income = pd.concat([projected_operating_income,
                                            pd.Series(terminal_operating_income)])
    projected_operating_income_after_tax = pd.concat([projected_operating_income_after_tax,
                                                      pd.Series(terminal_operating_income_after_tax)])
    projected_FCFF_value = pd.concat([projected_FCFF,
                                      pd.Series(terminal_value)])

    projected_FCFF = pd.concat([projected_FCFF,
                                pd.Series(terminal_FCFF)])

    projected_beta = pd.concat([projected_beta,
                                pd.Series(terminal_beta)])

    sales_to_capital_ratios = pd.concat([sales_to_capital_ratios,
                                pd.Series([terminal_sales_to_capital_ratio])])

    ### Add terminal cost of debt to the terminal year
    projected_after_tax_cost_of_debt_with_terminal = pd.concat([projected_after_tax_cost_of_debt,
                                                                pd.Series(projected_after_tax_cost_of_debt[-1:].values)])

    reinvestmentRate = projected_reinvestment/projected_operating_income_after_tax

    df_valuation = pd.DataFrame({"cumWACC":projected_cost_of_capital_cumulative_with_terminal_rate,
                                "cumCostOfEquity":projected_cost_of_equity_cumulative_with_terminal_rate,
                                'beta':projected_beta,
                                'ERP':ERP,
                                'projected_after_tax_cost_of_debt':projected_after_tax_cost_of_debt_with_terminal,
                                'revenueGrowth':projected_revenue_growth,
                                "revenues":projected_revenues,
                                "margins":projected_operating_margins,
                                'ebit':projected_operating_income,
                                "sales_to_capital_ratio":sales_to_capital_ratios,
                                "taxRate":projected_tax_rates,
                                'afterTaxOperatingIncome':projected_operating_income_after_tax,
                                "reinvestment":projected_reinvestment,
                                "invested_capital":invested_capital,
                                "ROIC":ROIC,
                                'reinvestmentRate':reinvestmentRate,
                                'FCFF':projected_FCFF,
                                'projected_FCFF_value':projected_FCFF_value})
    
    #### Add reinvestment rate and expected growth rate
    df_valuation['PVFCFF'] = df_valuation['FCFF']/df_valuation['cumWACC']
    value_of_operating_assets = df_valuation['PVFCFF'].sum()
    firm_value =  pd.Series(value_of_operating_assets + cash_and_non_operating_asset)[0]
    intrinsic_equity_present_value = firm_value - debt_value

    #### Future Frim, Debt and Equity Value
    cum_cost_of_debt_at_the_end_of_end_of_valuation =  (projected_after_tax_cost_of_debt+1).prod()
    cum_cost_of_capital_at_the_end_of_valuation =projected_cost_of_capital_cumulative[-1:].values[0]
    cum_cost_of_equity_at_the_end_of_valuation = projected_cost_of_equity_cumulative[-1:].values[0]

    ### FV Debt
    debt_future_value = cum_cost_of_debt_at_the_end_of_end_of_valuation * debt_value

    ### FV Frim
    firm_future_value = cum_cost_of_capital_at_the_end_of_valuation * cum_cost_of_capital_at_the_end_of_valuation

    ### FV Equity
    intrinsic_equity_future_value = intrinsic_equity_present_value * cum_cost_of_equity_at_the_end_of_valuation
    ## Returns
    def cum_return_calculator(value,
                            period,
                            append_nan=True):
        period = int(period)
        cum_return_series = pd.Series([1+value]*period).cumprod()
        if append_nan:
            cum_return_series = pd.concat([cum_return_series,pd.Series(np.nan)])
        return(cum_return_series)

    acceptable_annualized_return_on_equity = ((cum_cost_of_equity_at_the_end_of_valuation)**(1/valuation_interval_in_years))-1
    expected_annualized_return_on_equity = ((intrinsic_equity_future_value/equity_value)**(1/valuation_interval_in_years))-1
    excess_annualized_return_on_equity = ((intrinsic_equity_present_value/equity_value)**(1/valuation_interval_in_years))-1
    cum_acceptable_annualized_return_on_equity = cum_return_calculator(value = acceptable_annualized_return_on_equity,
                                                                       period = valuation_interval_in_years,
                                                                       append_nan=True)
    cum_expected_annualized_return_on_equity = cum_return_calculator(value = expected_annualized_return_on_equity,
                                                                       period = valuation_interval_in_years,
                                                                       append_nan=True)
    cum_excess_annualized_return_on_equity = cum_return_calculator(value = excess_annualized_return_on_equity,
                                                                       period = valuation_interval_in_years,
                                                                       append_nan=True)
    df_valuation['cum_acceptable_annualized_return_on_equity'] = cum_acceptable_annualized_return_on_equity
    df_valuation['cum_expected_annualized_return_on_equity'] = cum_expected_annualized_return_on_equity
    df_valuation['cum_excess_annualized_return_on_equity'] = cum_excess_annualized_return_on_equity
    df_valuation['cum_excess_annualized_return_on_equity_realized'] = df_valuation['cum_expected_annualized_return_on_equity']/df_valuation['cumCostOfEquity']
    df_valuation['excess_annualized_return_on_equity'] = pd.concat([pd.Series([excess_annualized_return_on_equity]*int(valuation_interval_in_years)),pd.Series(np.nan)])
    return({'valuation':df_valuation,
            'firm_value':firm_value,
            'equity_value':intrinsic_equity_present_value,
            'cash_and_non_operating_asset':cash_and_non_operating_asset,
            'debt_value':debt_value,
            'value_of_operating_assets':value_of_operating_assets})


########################################################
# POINT ESTIMATE DESCRIBER
########################################################

def point_estimate_describer(base_case_valuation):
    print('value of operating assets',np.round(base_case_valuation['value_of_operating_assets'],2),'\n',
        'cash and non operating asset',np.round(base_case_valuation['cash_and_non_operating_asset'],2),'\n',
        'debt value',np.round(base_case_valuation['debt_value'],2),'\n',
        'firm value',np.round(base_case_valuation['firm_value'],2),'\n',
        'Intrinsic Equity value',"${:.2f}".format(np.round(base_case_valuation['equity_value'],2)))
    df_valuation = base_case_valuation['valuation']
    df_valuation=  df_valuation.reset_index(drop=True)
    df_valuation['Year']= df_valuation.reset_index()['index']+1
    df_valuation.loc[df_valuation['Year'] == df_valuation['Year'].max(),"Year"] = 'Terminal'
    df_valuation= df_valuation.set_index("Year")
    return(df_valuation)


########################################################
# MONTE CARLO VALUATOR MULTI PHASE
########################################################

def monte_carlo_valuator_multi_phase(
    risk_free_rate,
    ERP,
    equity_value,
    debt_value,
    unlevered_beta,
    terminal_unlevered_beta,
    year_beta_begins_to_converge_to_terminal_beta,
    current_pretax_cost_of_debt,
    terminal_pretax_cost_of_debt,
    year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt,
    current_effective_tax_rate,
    marginal_tax_rate,
    year_effective_tax_rate_begin_to_converge_marginal_tax_rate,
    revenue_base,
    revenue_growth_rate_cycle1_begin,
    revenue_growth_rate_cycle1_end,
    revenue_growth_rate_cycle2_begin,
    revenue_growth_rate_cycle2_end,
    revenue_growth_rate_cycle3_begin,
    revenue_growth_rate_cycle3_end,
    revenue_convergance_periods_cycle1,
    revenue_convergance_periods_cycle2,
    revenue_convergance_periods_cycle3,
    length_of_cycle1,
    length_of_cycle2,
    length_of_cycle3,
    current_sales_to_capital_ratio,
    terminal_sales_to_capital_ratio,
    year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital,
    current_operating_margin,
    terminal_operating_margin,
    year_operating_margin_begins_to_converge_to_terminal_operating_margin,
    additional_return_on_cost_of_capital_in_perpetuity,
    cash_and_non_operating_asset,
    asset_liquidation_during_negative_growth,
    current_invested_capital,
    sample_size=1000,
    list_of_correlation_between_variables=[['additional_return_on_cost_of_capital_in_perpetuity','terminal_sales_to_capital_ratio',0.4],
                                           ['additional_return_on_cost_of_capital_in_perpetuity','terminal_operating_margin',.6]]):
    variables_distributsion = [risk_free_rate,
                                   ERP,
                                   equity_value,
                                   debt_value,
                                   unlevered_beta,
                                    terminal_unlevered_beta,
                                    year_beta_begins_to_converge_to_terminal_beta,
                                    current_pretax_cost_of_debt,
                                    terminal_pretax_cost_of_debt,
                                    year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt,
                                    current_effective_tax_rate,
                                    marginal_tax_rate,
                                    year_effective_tax_rate_begin_to_converge_marginal_tax_rate,
                                    revenue_base,
                                    revenue_growth_rate_cycle1_begin,
                                    revenue_growth_rate_cycle1_end,
                                    revenue_growth_rate_cycle2_begin,
                                    revenue_growth_rate_cycle2_end,
                                    revenue_growth_rate_cycle3_begin,
                                    revenue_growth_rate_cycle3_end,
                                    revenue_convergance_periods_cycle1,
                                    revenue_convergance_periods_cycle2,
                                    revenue_convergance_periods_cycle3,
                                    length_of_cycle1,
                                    length_of_cycle2,
                                    length_of_cycle3,
                                    current_sales_to_capital_ratio,
                                    terminal_sales_to_capital_ratio,
                                    year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital,
                                    current_operating_margin,
                                    terminal_operating_margin,
                                    year_operating_margin_begins_to_converge_to_terminal_operating_margin,
                                    additional_return_on_cost_of_capital_in_perpetuity,
                                    cash_and_non_operating_asset,
                                    asset_liquidation_during_negative_growth,
                                    current_invested_capital]
    variable_names = ['risk_free_rate',
                                   'ERP',
                                   'equity_value',
                                   'debt_value',
                                   'unlevered_beta',
                                    'terminal_unlevered_beta',
                                    'year_beta_begins_to_converge_to_terminal_beta',
                                    'current_pretax_cost_of_debt',
                                    'terminal_pretax_cost_of_debt',
                                    'year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt',
                                    'current_effective_tax_rate',
                                    'marginal_tax_rate',
                                    'year_effective_tax_rate_begin_to_converge_marginal_tax_rate',
                                    'revenue_base',
                                    'revenue_growth_rate_cycle1_begin',
                                    'revenue_growth_rate_cycle1_end',
                                    'revenue_growth_rate_cycle2_begin',
                                    'revenue_growth_rate_cycle2_end',
                                    'revenue_growth_rate_cycle3_begin',
                                    'revenue_growth_rate_cycle3_end',
                                    'revenue_convergance_periods_cycle1',
                                    'revenue_convergance_periods_cycle2',
                                    'revenue_convergance_periods_cycle3',
                                    'length_of_cycle1',
                                    'length_of_cycle2',
                                    'length_of_cycle3',
                                    'current_sales_to_capital_ratio',
                                    'terminal_sales_to_capital_ratio',
                                    'year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital',
                                    'current_operating_margin',
                                    'terminal_operating_margin',
                                    'year_operating_margin_begins_to_converge_to_terminal_operating_margin',
                                    'additional_return_on_cost_of_capital_in_perpetuity',
                                    'cash_and_non_operating_asset',
                                    'asset_liquidation_during_negative_growth',
                                    'current_invested_capital']
    ### The following variable  should have "year" in their definition but I did not think of ut. So I am adding them to list_of_columns_with_year_to_be_int
    list_of_columns_with_year_to_be_int = [s for s in variable_names if "year" in s] +['length_of_cycle1','length_of_cycle2','length_of_cycle3',
                                                                                       'revenue_convergance_periods_cycle1',
                                                                                       'revenue_convergance_periods_cycle2','revenue_convergance_periods_cycle3']
    ### Build a DataFarame to have index - location of each variable in the correlation matrix
    dict_of_varible = dict(zip(variable_names,
                            range(0,len(variable_names))))
    df_variables = pd.DataFrame([dict_of_varible])

    ### Initaile Correlation Matrix
    R = ot.CorrelationMatrix(len(variables_distributsion))
    ### pair correlation between each variable
    for pair_of_variable in list_of_correlation_between_variables:
        location = df_variables[pair_of_variable[:2]].values[0]
        #print(location)
        R[int(location[0]),int(location[1])] = pair_of_variable[2]

    ### Build the correlation into composed distribution function
    ### For ot.NormalCopula The correlation matrix must be definite positive
    ### Here is an implementaion on how to get the nearest psd matirx https://stackoverflow.com/questions/43238173/python-convert-matrix-to-positive-semi-definite
    copula = ot.NormalCopula(R)
    BuiltComposedDistribution = ot.ComposedDistribution(variables_distributsion,
                                                        copula)
    ### Generate samples
    generated_sample = BuiltComposedDistribution.getSample(sample_size)
    df_generated_sample = pd.DataFrame.from_records(generated_sample, columns= variable_names)
    df_generated_sample[list_of_columns_with_year_to_be_int] = df_generated_sample[list_of_columns_with_year_to_be_int].apply(lambda x: round(x))
    print("Scenario Generation Complete", df_generated_sample.shape)
    df_generated_sample['full_valuation']= df_generated_sample.apply(lambda row:
                                                                    valuator_multi_phase(
                                                                        risk_free_rate = row['risk_free_rate'],
                                                                        ERP = row['ERP'],
                                                                        equity_value = row['equity_value'],
                                                                        debt_value = row['debt_value'],
                                                                        unlevered_beta = row['unlevered_beta'],
                                                                        terminal_unlevered_beta = row['terminal_unlevered_beta'],
                                                                        year_beta_begins_to_converge_to_terminal_beta = row['year_beta_begins_to_converge_to_terminal_beta'],
                                                                        current_pretax_cost_of_debt = row['current_pretax_cost_of_debt'],
                                                                        terminal_pretax_cost_of_debt = row['terminal_pretax_cost_of_debt'],
                                                                        year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt = row['year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt'],
                                                                        current_effective_tax_rate = row['current_effective_tax_rate'],
                                                                        marginal_tax_rate = row['marginal_tax_rate'],
                                                                        year_effective_tax_rate_begin_to_converge_marginal_tax_rate = row['year_effective_tax_rate_begin_to_converge_marginal_tax_rate'],
                                                                        revenue_base = row['revenue_base'],
                                                                        revenue_growth_rate_cycle1_begin = row['revenue_growth_rate_cycle1_begin'],
                                                                        revenue_growth_rate_cycle1_end = row['revenue_growth_rate_cycle1_end'],
                                                                        revenue_growth_rate_cycle2_begin = row['revenue_growth_rate_cycle2_begin'],
                                                                        revenue_growth_rate_cycle2_end = row['revenue_growth_rate_cycle2_end'],
                                                                        revenue_growth_rate_cycle3_begin = row['revenue_growth_rate_cycle3_begin'],
                                                                        revenue_growth_rate_cycle3_end = row['revenue_growth_rate_cycle3_end'],
                                                                        revenue_convergance_periods_cycle1 = row['revenue_convergance_periods_cycle1'],
                                                                        revenue_convergance_periods_cycle2 = row['revenue_convergance_periods_cycle2'],
                                                                        revenue_convergance_periods_cycle3 = row['revenue_convergance_periods_cycle3'],
                                                                        length_of_cycle1 = row['length_of_cycle1'],
                                                                        length_of_cycle2 = row['length_of_cycle2'],
                                                                        length_of_cycle3 = row['length_of_cycle3'],
                                                                        current_sales_to_capital_ratio = row['current_sales_to_capital_ratio'],
                                                                        terminal_sales_to_capital_ratio = row['terminal_sales_to_capital_ratio'],
                                                                        year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital = row['year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital'],
                                                                        current_operating_margin = row['current_operating_margin'],
                                                                        terminal_operating_margin = row['terminal_operating_margin'],
                                                                        year_operating_margin_begins_to_converge_to_terminal_operating_margin = row['year_operating_margin_begins_to_converge_to_terminal_operating_margin'],
                                                                        additional_return_on_cost_of_capital_in_perpetuity = row['additional_return_on_cost_of_capital_in_perpetuity'],
                                                                        cash_and_non_operating_asset = row['cash_and_non_operating_asset'],
                                                                        asset_liquidation_during_negative_growth=row['asset_liquidation_during_negative_growth'],
                                                                        current_invested_capital=row['current_invested_capital']),
                                                                        axis=1)
    ### extract the valuation result
    df_generated_sample['valuation'] = df_generated_sample['full_valuation'].apply(lambda x: x['valuation'])
    df_generated_sample['equity_valuation'] = df_generated_sample['full_valuation'].apply(lambda x: x['equity_value'])
    df_generated_sample['firm_valuation'] = df_generated_sample['full_valuation'].apply(lambda x: x['firm_value'])
    df_generated_sample['terminal_revenue'] = df_generated_sample['valuation'].apply(lambda x: x['revenues'].values[-1])
    df_generated_sample['terminal_operating_margin'] = df_generated_sample['valuation'].apply(lambda x: x['margins'].values[-1])
    df_generated_sample['terminal_reinvestmentRate'] = df_generated_sample['valuation'].apply(lambda x: x['reinvestmentRate'].values[-1])
    df_generated_sample['terminal_afterTaxOperatingIncome'] = df_generated_sample['valuation'].apply(lambda x: x['afterTaxOperatingIncome'].values[-1])
    df_generated_sample['terminal_FCFF'] = df_generated_sample['valuation'].apply(lambda x: x['FCFF'].values[-1])
    df_generated_sample['cumWACC'] = df_generated_sample['valuation'].apply(lambda x: x['cumWACC'][:-1].values)
    df_generated_sample['cumCostOfEquity'] = df_generated_sample['valuation'].apply(lambda x: x['cumCostOfEquity'][:-1].values)
    df_generated_sample['cum_acceptable_annualized_return_on_equity'] = df_generated_sample['valuation'].apply(lambda x: x['cum_acceptable_annualized_return_on_equity'][:-1].values)
    df_generated_sample['cum_expected_annualized_return_on_equity'] = df_generated_sample['valuation'].apply(lambda x: x['cum_expected_annualized_return_on_equity'][:-1].values)
    df_generated_sample['cum_excess_annualized_return_on_equity'] = df_generated_sample['valuation'].apply(lambda x: x['cum_excess_annualized_return_on_equity'][:-1].values)
    df_generated_sample['cum_excess_annualized_return_on_equity_realized'] = df_generated_sample['valuation'].apply(lambda x: x['cum_excess_annualized_return_on_equity_realized'][:-1].values)
    df_generated_sample['excess_annualized_return_on_equity'] = df_generated_sample['valuation'].apply(lambda x: x['excess_annualized_return_on_equity'][:-1].values)
    df_generated_sample['ROIC'] = df_generated_sample['valuation'].apply(lambda x: x['ROIC'][:-1].values)
    df_generated_sample['invested_capital'] = df_generated_sample['valuation'].apply(lambda x: x['invested_capital'][:-1].values)
    return(df_generated_sample)


########################################################
# VALUATION DESCRIBER
########################################################

def histogram_plotter_plotly(
        data,
        column_name,
        xlabel,
        title='Data',
        bins=30,
        percentile=[15, 50, 85],
        color=['#A2AF9B', '#DCCFC0', '#242424'],
        histnorm='percent',
        marginal=None,
        height=700,
        width=800
    ):
    import plotly.graph_objects as go
    import plotly.express as px
    import numpy as np

    fig = px.histogram(
        data,
        x=column_name,
        histnorm=histnorm,
        nbins=bins,
        labels={column_name: xlabel.title()},
        marginal=marginal,
        color_discrete_sequence=['#A2AF9B']
    )

    # Estimate y_max for drawing vertical lines
    n, _ = np.histogram(data[column_name], bins=bins, density=False)
    y_max = np.max(n / n.sum()) * 100 * 1.65

    # Add percentile lines
    for i in range(len(percentile)):
        percentile_value = np.percentile(data[column_name], percentile[i])
        fig.add_trace(go.Scatter(
            x=[percentile_value, percentile_value],
            y=(0, y_max),
            mode="lines",
            name=f"P{percentile[i]}",
            marker=dict(color=color[i])
        ))

    # Apply transparent theme settings inline
    fig.update_layout(
        height=height,
        width=width,
        title=dict(
            text=title.title(),
            font=dict(color="#242424")
        ),
        xaxis=dict(
            title=dict(text=xlabel.title()),
            color="#242424",
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text=("Density" if histnorm == "density" else "Percent").title()),
            color="#242424",
            showgrid=False
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="system-ui, Avenir, Helvetica, Arial, sans-serif",
            color="#242424"
        ),
        legend=dict(
            orientation="v",
            x=1,
            y=0.1,
            xanchor='right',
            yanchor='bottom',
            bgcolor='rgba(0,0,0,0)',
            font=dict(color="#242424")
        )
    )

    return fig


########################################################
# ECDF PLOTTER
########################################################

def ecdf_plotter_plotly(
        data,
        column_name,
        xlabel,
        title='Data',
        percentile=[15, 50, 85],
        color=['#A2AF9B', '#DCCFC0', '#242424'],
        marginal=None,
        height=700,
        width=800
    ):
    """Plot ECDF via Plotly"""
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np

    fig = px.ecdf(
        data,
        x=column_name,
        labels={column_name: xlabel.title()},
        marginal=marginal
    )

    # Update histogram trace styling (if any)
    for trace in fig.data:
        if trace.type == "histogram":
            trace.update(
                marker=dict(
                    color='rgb(59, 117, 175)',
                    line=dict(width=0)
                ),
                opacity=1.0
            )

    # Add percentile lines
    for i in range(len(percentile)):
        fig.add_trace(go.Scatter(
            x=[np.percentile(data[column_name], percentile[i])] * 2,
            y=[0, 1],
            mode="lines",
            name=f"P{percentile[i]}",
            marker=dict(color=color[i])
        ))

    # Dummy legend entry
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode="lines",
        name="Current Market Cap",
        line=dict(color="#242424", dash="dash"),
        showlegend=True
    ))

    # Transparent theme and base layout
    fig.update_layout(
        height=height,
        width=width,
        title=dict(
            text=title.title(),
            font=dict(color="#242424")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="system-ui, Avenir, Helvetica, Arial, sans-serif",
            color="#242424"
        ),
        legend=dict(
            orientation="v",
            x=1,
            y=0.1,
            xanchor='right',
            yanchor='bottom',
            bgcolor='rgba(0,0,0,0)',
            font=dict(color="#242424")
        )
    )

    # Remove all axis grids efficiently (including marginal subplots)
    for axis in fig.layout:
        if axis.startswith('xaxis') or axis.startswith('yaxis'):
            fig.layout[axis].update(
                showgrid=False,
                zeroline=False,
                gridcolor="rgba(0,0,0,0)"
            )

    return fig


def time_series_plotly(df_data,
                       x,
                       yleft,
                       yright,
                       height=700,
                       width=800,
                       title=None):
    """ Graph 2 time series on 2 different y-axis"""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df_data[x], y=df_data[yleft], name=yleft),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df_data[x], y=df_data[yright], name=yright),
        secondary_y=True,
    )
    fig = fig.update_layout(height=height, width=width,title=title)
    return(fig)

########################################################
# PLOTLY LINE BAR CHART
########################################################

def plotly_line_bar_chart(df_data,
                       x,
                       ybar,
                       yline,
                       height=700,
                       width=800,
                       rangemode=None,
                       title=None):
    """ Graph 2 time series on 2 different y-axis"""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig.update_yaxes(rangemode='tozero')

    for bar_var in ybar:
        # Add traces
        fig.add_trace(
            go.Bar(x=df_data[x], y=df_data[bar_var],name=bar_var),
            secondary_y=False
            )
    #fig.update_yaxes(rangemode='tozero')
    for line_var in yline:
        fig.add_trace(
            go.Scatter(x=df_data[x], y=df_data[line_var],name=line_var),
            secondary_y=True,
            )
    if rangemode != None:
        fig.update_yaxes(rangemode=rangemode)
    fig = fig.update_layout(height=height, width=width,title=title)
    return(fig)

########################################################
# PLOTLY LINE DASH BAR CHART
########################################################

def plotly_line_dash_bar_chart(
        df_data,
        x,
        ybar,
        yline,
        ydash,
        height=700,
        width=800,
        rangemode=None,
        title=None,
        barmode='group'
    ):
    """Graph 2 time series on 2 different y-axes with transparent styling."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar traces on left axis
    for bar_var in ybar:
        fig.add_trace(
            go.Bar(
                x=df_data[x],
                y=df_data[bar_var],
                name=bar_var.replace("_", " ").title().replace("50%", "(P50)"),
                marker=dict(color='#A2AF9B')
            ),
            secondary_y=False,
        )

    # Solid line traces on right axis
    for line_var in yline:
        fig.add_trace(
            go.Scatter(
                x=df_data[x],
                y=df_data[line_var],
                name=line_var.replace("50%", "(P50)")
            ),
            secondary_y=True,
        )

    # Dashed line traces on right axis
    for dash_var in ydash:
        fig.add_trace(
            go.Scatter(
                x=df_data[x],
                y=df_data[dash_var],
                name=dash_var,
                line=dict(dash='dot')
            ),
            secondary_y=True,
        )

    # Optional y-axis range mode
    if rangemode is not None:
        fig.update_yaxes(rangemode=rangemode)

    # Apply transparent layout styling
    fig.update_layout(
        height=height,
        width=width,
        title=dict(
            text=title,
            font=dict(color="#242424")
        ),
        barmode=barmode,
        xaxis=dict(
            title=dict(text="Year"),
            color="#242424",
            showgrid=False
        ),
        yaxis=dict(
            title=dict(text="Invested Capital"),
            color="#242424",
            showgrid=False
        ),
        yaxis2=dict(
            title=dict(text="ROIC"),
            side="right",
            color="#242424",
            showgrid=False
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="system-ui, Avenir, Helvetica, Arial, sans-serif",
            color="#242424"
        ),
        legend=dict(
            x=0,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            font=dict(color="#242424")
        )
    )

    return fig


########################################################
# PLOTLY LINE WITH ERROR BOUND
########################################################

def line_plotter_with_error_bound(df_data,
                                  x,
                                  list_of_mid_point,
                                  list_of_lower_bound,
                                  list_of_upper_bound,
                                  list_of_bar=[],
                                  list_of_name=[],
                                  list_of_fillcolor=['rgba(68, 68, 68, 0.3)'],
                                  list_of_line_color=['rgb(31, 119, 180)'],
                                  title=None,
                                  yaxis_title=None,
                                  height=700,
                                  width=800):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Round selected columns
    cols_to_round = list(set(
        [x] +
        list_of_mid_point +
        list_of_lower_bound +
        list_of_upper_bound +
        list_of_bar
    ))
    df_data[cols_to_round] = df_data[cols_to_round].round(4)

    # Create figure
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add line + error bounds
    for mid_point, lower_bound, upper_bound, name, fillcolor, line_color in zip(
        list_of_mid_point, list_of_lower_bound, list_of_upper_bound,
        list_of_name, list_of_fillcolor, list_of_line_color):

        display_name = name.replace("_", " ").title().replace(" 50%", " (P50)")

        fig.add_trace(
            go.Scatter(
                name=display_name,
                x=df_data[x],
                y=df_data[mid_point],
                mode='lines',
                line=dict(color=line_color),
                hovertemplate=f"%{{x}}<br>{name}: %{{y:.2f}}<extra></extra>"
            )
        )

        fig.add_trace(
            go.Scatter(
                name=name + ' UB',
                x=df_data[x],
                y=df_data[upper_bound],
                mode='lines',
                marker=dict(color=line_color),
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip"
            )
        )

        fig.add_trace(
            go.Scatter(
                name=name + ' LB',
                x=df_data[x],
                y=df_data[lower_bound],
                mode='lines',
                marker=dict(color=line_color),
                line=dict(width=0),
                fillcolor=fillcolor,
                fill='tonexty',
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # Add bars
    for bar_var in list_of_bar:
        formatted_name = bar_var.replace("_", " ").title().replace(" 50%", " (P50)")
        fig.add_trace(
            go.Bar(
                x=df_data[x],
                y=df_data[bar_var],
                name=formatted_name,
                marker=dict(color='rgb(59, 117, 175)'),
                opacity=1.0,
                hovertemplate=f"%{{x}}<br>{formatted_name}: %{{y:.2f}}<extra></extra>"
            ),
            secondary_y=True
        )

    # Update layout with transparent theme
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(color="#242424")
        ),
        xaxis=dict(
            title=dict(text="Year"),
            color="#242424",
            showgrid=False,
            tickformat=".2f"
        ),
        yaxis=dict(
            title=dict(text=yaxis_title),
            color="#242424",
            showgrid=False,
            tickformat=".2f"
        ),
        yaxis2=dict(
            title=dict(text="Excess Annualized Return"),
            side="right",
            tickformat=".2f",
            color="#242424",
            showgrid=False,
            range=[-.05, .3]
        ),
        font=dict(
            family="system-ui, Avenir, Helvetica, Arial, sans-serif",
            color="#242424"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            x=0,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#242424')
        ),
        hovermode="x",
        height=height,
        width=width
    )

    return fig




########################################################
# RETURN VALUES FROM LIST EXTRACTOR
########################################################

def return_values_from_list_extractor(df_data,
                                        col,
                                        add_1=True):
    "This function is to get the cost stats of specied col by year"
    df_cost_of_cap = pd.DataFrame(list(df_data[col].values))
    if add_1:
        df_cost_of_cap[-1] = 1.00
    else:
        df_cost_of_cap[-1] = 0
    df_cost_of_cap = pd.melt(
        df_cost_of_cap,
        var_name='year',
        value_name=col
    ).dropna()
    df_cost_of_cap = df_cost_of_cap.groupby(['year'])[[col]].describe().reset_index()
    df_cost_of_cap = data_frame_flattener(df_cost_of_cap)
    df_cost_of_cap = df_cost_of_cap.set_index("year")
    return(df_cost_of_cap)


########################################################
# RETURN VALUES FROM LIST EXTRACTOR STEP 2
########################################################

def return_values_from_list_extractor_step2(df_data,
                                            cum_ret_col,
                                            ret_col):
    list_of_df_return = []
    for col in cum_ret_col:
        df_res = return_values_from_list_extractor(df_data,
                                                   col=col)
        list_of_df_return.append(df_res)
    for col in ret_col:
        df_res = return_values_from_list_extractor(df_data,
                                                   col=col,
                                                   add_1=False)
        list_of_df_return.append(df_res)
    df_returns = pd.concat(list_of_df_return,axis=1)
    df_returns = df_returns.reset_index(drop=True).reset_index().rename(columns={"index":"year"})
    return(df_returns)


########################################################
# VALUATION DESCRIBER
########################################################

def valuation_describer(df_intc_valuation,
                        sharesOutstanding=1):
    
    """Describe stats of monte dcf carlo simulation"""

    ### Get the Equity value at each percentile
    current_market_cap = df_intc_valuation['equity_value'].median()
    percentiles=np.arange(0, 110, 10)
    equity_value_at_each_percentile = np.percentile(df_intc_valuation['equity_valuation'],
                                                    percentiles)
    df_valuation_res = pd.DataFrame({"percentiles":percentiles,
                                     "equity_value":equity_value_at_each_percentile})
    df_valuation_res['current_market_cap'] = current_market_cap
    df_valuation_res['current_price_per_share'] = current_market_cap/sharesOutstanding
    df_valuation_res['equity_value_per_share'] = df_valuation_res['equity_value']/sharesOutstanding
    df_valuation_res['Price/Value']= df_valuation_res['current_market_cap']/df_valuation_res['equity_value']
    df_valuation_res['PNL']= (df_valuation_res['equity_value']/df_valuation_res['current_market_cap'])-1
    
    ### Histogram
    fig = histogram_plotter_plotly(
        data=df_intc_valuation,
        column_name ='equity_valuation',
        xlabel ='Market Cap',
        title='Intrinsic Equity Value Distribution',
        bins=200,
        percentile=[15,50,85],
        color=['green','yellow','red'],
        histnorm='percent',
        height=700,
        width=800
    )
    
    fig = fig.add_vline(
        x = current_market_cap, 
        line_dash = 'dash',
        line_color='#242424',
        annotation_text=" Current Market Cap",
        annotation_font_size=12,
        annotation_font_color='#242424'
    )
    
    ### Plot cummultaive distribution of intrincsict equity value
    fig_cdf = ecdf_plotter_plotly(
        data=df_intc_valuation,
        column_name ='equity_valuation',
        xlabel ='Market Cap',
        title='Intrinsic Equity Value Cumulative Distribution',
        percentile=[15,50,85],
        color=['green','yellow','red'],
        marginal='histogram',
        height=700,
        width=800
        )
    
    fig_cdf = fig_cdf.add_vline(
        x=current_market_cap, 
        line_dash = 'dash',
        line_color='#242424'
    )

    #### Return on Investment
    df_returns = return_values_from_list_extractor_step2(
        df_intc_valuation,
        cum_ret_col = [
            'cumWACC', 
            'cumCostOfEquity',
            'cum_acceptable_annualized_return_on_equity',
            'cum_expected_annualized_return_on_equity',
            'cum_excess_annualized_return_on_equity',
            'cum_excess_annualized_return_on_equity_realized'
        ],
        ret_col=['excess_annualized_return_on_equity']
    )

    ### Plot returns
    fig_return = line_plotter_with_error_bound(
        df_data = df_returns,
        x='year',
        list_of_mid_point = ['cum_expected_annualized_return_on_equity 50%','cumCostOfEquity 50%'],
        list_of_lower_bound = ['cum_expected_annualized_return_on_equity min','cumCostOfEquity min'],
        list_of_upper_bound = ['cum_expected_annualized_return_on_equity max','cumCostOfEquity max'],
        list_of_bar=['excess_annualized_return_on_equity 50%'],
        list_of_name=['Cum Expected Return','Cost of Equity'],
        list_of_fillcolor= ['rgba(59, 237, 157, 0.5)','rgba(255,84,167, 0.3)'],
        list_of_line_color= ['rgb(37, 162, 111)','rgb(238, 72, 103)'],
        title='Return on Equity Investment',
        yaxis_title='Cum Return',
        height=700,
        width=800
    )
    
    #### ROIC and Invested Capital
    df_roic = return_values_from_list_extractor_step2(
        df_data = df_intc_valuation,
        cum_ret_col = [],
        ret_col = ['ROIC','invested_capital']
    )[1:]

    fig_roic_inv = plotly_line_dash_bar_chart(
        df_roic,
        x='year',
        ybar=['invested_capital 50%'],
        yline=['ROIC 50%'],
        ydash=[],
        height=700,
        width=800,
        rangemode=None,
        title='Simulated Median ROIC and Invested Capital',
        barmode='group'
    )
    
    def to_centered_html(fig):
        html = to_html(
            fig,
            include_plotlyjs="cdn",
            full_html=True,
            config={
                "responsive": False,
                "displayModeBar": False,
                "displaylogo": False
            }
        )
        # Inject CSS to center the figure's div
        centered_style = """
        <style>
        body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        div.js-plotly-plot { margin: auto; }
        </style>
        """
        return html.replace("</head>", centered_style + "</head>")
    
    valuation_summary = df_valuation_res.to_dict(orient="records")
    valuation_summary_filtered = filter(lambda x: x['percentiles'] in [20, 50, 80], valuation_summary)
    
    charts = {
        "valuation_summary": list(valuation_summary_filtered),
        "plots": {
            "histogram": {
                "html": to_centered_html(fig)
            },
            "cdf": {
                "html": to_centered_html(fig_cdf)
            },
            "roic": {
                "html": to_centered_html(fig_roic_inv)
            },
            "return": {
                "html": to_centered_html(fig_return)
            }
        }
    }
    return charts


########################################################
# ADJUST PARAMETERS INPUT TO API
########################################################

def adjust_parameters_input_to_api(input_list):
    monte_carlo_input = {
        "sample_size": 10000,
        "list_of_correlation_between_variables": [
        # Intuitive / common sense correlations
        ['revenue_growth_rate_cycle3_end', 'risk_free_rate', 0.95],
        ['revenue_growth_rate_cycle3_end', 'terminal_pretax_cost_of_debt', 0.9],
        ['terminal_pretax_cost_of_debt', 'risk_free_rate', 0.9],

        # Valuation-specific correlations
        ['ERP', 'revenue_growth_rate_cycle2_begin', 0.4],
        ['ERP', 'revenue_growth_rate_cycle2_end', 0.4],
        ['ERP', 'revenue_growth_rate_cycle3_begin', 0.4],
        ['additional_return_on_cost_of_capital_in_perpetuity', 'terminal_sales_to_capital_ratio', 0.25],
        ['additional_return_on_cost_of_capital_in_perpetuity', 'terminal_operating_margin', 0.5],
        ['terminal_sales_to_capital_ratio', 'terminal_operating_margin', 0.3],
    ]
    }
    shares_outstanding = None
    for dict in input_list:
        value = None
        if dict["distribution"] == "normal":
            value = ot.Normal(dict["values"]["mean"], dict["values"]["std"])
            monte_carlo_input[dict["id"]] = value
        elif dict["distribution"] == "triangular":
            value = ot.Triangular(dict["values"]["min"], dict["values"]["mode"], dict["values"]["max"])
            monte_carlo_input[dict["id"]] = value
        elif dict["distribution"] == "uniform":
            value = ot.Uniform(dict["values"]["low"], dict["values"]["high"])
            monte_carlo_input[dict["id"]] = value
        elif dict["distribution"] == "skewnorm":
            value = ot.Distribution(ot.SciPyDistribution(scipy.stats.skewnorm(dict["values"]["skewness"], loc=dict["values"]["loc"], scale=dict["values"]["scale"])))
            monte_carlo_input[dict["id"]] = value
        if dict["id"] == "shares_outstanding":
            shares_outstanding = dict["values"]["constant"]
    return monte_carlo_input, shares_outstanding
