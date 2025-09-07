import { useState } from "react";

function DCFForm() {
  const [expandedSection, setExpandedSection] = useState(null);

  const toggleSection = (section) => {
    if (expandedSection === section) {
      setExpandedSection(null);
    } else {
      setExpandedSection(section);
    }
  };

  const handleInputChange = (sectionId, itemId, field, value) => {
    setSections((prevSections) => {
      return prevSections.map((section) => {
        if (section.id === sectionId) {
          return {
            ...section,
            content: section.content.map((item) => {
              if (item.id === itemId) {
                return {
                  ...item,
                  [field]: parseFloat(value) || 0,
                };
              }
              return item;
            }),
          };
        }
        return section;
      });
    });
  };

  const [sections, setSections] = useState([
    {
      id: "capitalStructure",
      title: "Capital Structure",
      content: [
        {
          id: "risk_free_rate",
          label: "Risk Free Rate",
          distribution: "normal",
          mean: 0.04,
          std: 0.002,
        },
        {
          id: "ERP",
          label: "ERP",
          distribution: "normal",
          mean: 0.048,
          std: 0.001,
        },
        {
          id: "equity_value",
          label: "Equity Value",
          distribution: "triangular",
          min: 45,
          mode: 51.016,
          max: 57,
        },
        {
          id: "debt_value",
          label: "Debt Value",
          distribution: "triangular",
          min: 3.7,
          mode: 3.887,
          max: 4,
        },
        {
          id: "unlevered_beta",
          label: "Unlevered Beta",
          distribution: "triangular",
          min: 0.8,
          mode: 0.9,
          max: 1,
        },
        {
          id: "terminal_unlevered_beta",
          label: "Terminal Unlevered Beta",
          distribution: "triangular",
          min: 0.8,
          mode: 0.9,
          max: 1,
        },
        {
          id: "year_beta_begins_to_converge_to_terminal_beta",
          label: "Year Beta Begins To Converge To Terminal Beta",
          distribution: "uniform",
          low: 1,
          high: 2,
        },
      ],
    },
    {
      id: "costOfCapital",
      title: "Cost of Capital",
      content: [
        {
          id: "current_pretax_cost_of_debt",
          label: "Current Pretax Cost Of Debt",
          distribution: "triangular",
          min: 0.057,
          mode: 0.06,
          max: 0.063,
        },
        {
          id: "terminal_pretax_cost_of_debt",
          label: "Terminal Pretax Cost Of Debt",
          distribution: "triangular",
          min: 0.052,
          mode: 0.055,
          max: 0.058,
        },
        {
          id: "year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt",
          label: "Year Cost Of Debt Begins To Converge To Terminal Value",
          distribution: "uniform",
          low: 1,
          high: 2,
        },
        {
          id: "current_effective_tax_rate",
          label: "Current Effective Tax Rate",
          distribution: "triangular",
          min: 0.23,
          mode: 0.24,
          max: 0.25,
        },
        {
          id: "marginal_tax_rate",
          label: "Marginal Tax Rate",
          distribution: "triangular",
          min: 0.23,
          mode: 0.25,
          max: 0.27,
        },
        {
          id: "year_effective_tax_rate_begin_to_converge_marginal_tax_rate",
          label: "Year Effective Tax Rate Begin To Converge Marginal Tax Rate",
          distribution: "uniform",
          low: 1,
          high: 3,
        },
        {
          id: "additional_return_on_cost_of_capital_in_perpetuity",
          label: "Additional Return On Cost Of Capital In Perpetuity",
          distribution: "triangular",
          min: 0.0,
          mode: 0.02,
          max: 0.035,
        },
      ],
    },
    {
      id: "revenueGrowth",
      title: "Revenue Growth Assumptions",
      content: [
        {
          id: "revenue_base",
          label: "Revenue Base",
          distribution: "triangular",
          min: 8.8,
          mode: 9.2,
          max: 9.6,
        },
        {
          id: "revenue_growth_rate_cycle1_begin",
          label: "Revenue Growth Rate Cycle 1 Begin",
          distribution: "skewnorm",
          skewness: -2.9,
          loc: 0.145,
          scale: 0.032,
        },
        {
          id: "revenue_growth_rate_cycle1_end",
          label: "Revenue Growth Rate Cycle 1 End",
          distribution: "skewnorm",
          skewness: -2.9,
          loc: 0.18,
          scale: 0.033,
        },
      ],
    },
    {
      id: "revenueTiming",
      title: "Revenue Timing Assumptions",
      content: [
        {
          id: "length_of_cycle1",
          label: "Length of Cycle 1",
          distribution: "uniform",
          low: 4,
          high: 8,
        },
        {
          id: "revenue_growth_rate_cycle2_begin",
          label: "Revenue Growth Rate Cycle 2 Begin",
          distribution: "skewnorm",
          skewness: -2.9,
          loc: 0.165,
          scale: 0.034,
        },
        {
          id: "revenue_growth_rate_cycle2_end",
          label: "Revenue Growth Rate Cycle 2 End",
          distribution: "skewnorm",
          skewness: -2.9,
          loc: 0.11,
          scale: 0.032,
        },
        {
          id: "length_of_cycle2",
          label: "Length of Cycle 2",
          distribution: "uniform",
          low: 4,
          high: 8,
        },
        {
          id: "revenue_growth_rate_cycle3_begin",
          label: "Revenue Growth Rate Cycle 3 Begin",
          distribution: "skewnorm",
          skewness: -2.9,
          loc: 0.09,
          scale: 0.024,
        },
        {
          id: "revenue_growth_rate_cycle3_end",
          label: "Revenue Growth Rate Cycle 3 End",
          distribution: "normal",
          mean: 0.04,
          std: 0.002,
        },
        {
          id: "length_of_cycle3",
          label: "Length of Cycle 3",
          distribution: "uniform",
          low: 4,
          high: 8,
        },
        {
          id: "revenue_convergance_periods_cycle1",
          label: "Revenue Convergence Periods Cycle 1",
          distribution: "uniform",
          low: 1,
          high: 2,
        },
        {
          id: "revenue_convergance_periods_cycle2",
          label: "Revenue Convergence Periods Cycle 2",
          distribution: "uniform",
          low: 1,
          high: 2,
        },
        {
          id: "revenue_convergance_periods_cycle3",
          label: "Revenue Convergence Periods Cycle 3",
          distribution: "uniform",
          low: 1,
          high: 2,
        },
      ],
    },
    {
      id: "operatingEfficiency",
      title: "Operating Efficiency & Profitability",
      content: [
        {
          id: "current_sales_to_capital_ratio",
          label: "Current Sales to Capital Ratio",
          distribution: "triangular",
          min: 1.5,
          mode: 1.7,
          max: 1.9,
        },
        {
          id: "terminal_sales_to_capital_ratio",
          label: "Terminal Sales to Capital Ratio",
          distribution: "triangular",
          min: 1.1,
          mode: 1.3,
          max: 1.6,
        },
        {
          id: "year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital",
          label: "Year Sales to Capital Begins to Converge to Terminal Value",
          distribution: "uniform",
          low: 1,
          high: 3,
        },
        {
          id: "current_operating_margin",
          label: "Current Operating Margin",
          distribution: "triangular",
          min: 0.145,
          mode: 0.15,
          max: 0.155,
        },
        {
          id: "terminal_operating_margin",
          label: "Terminal Operating Margin",
          distribution: "triangular",
          min: 0.12,
          mode: 0.175,
          max: 0.22,
        },
        {
          id: "year_operating_margin_begins_to_converge_to_terminal_operating_margin",
          label: "Year Operating Margin Begins to Converge to Terminal Value",
          distribution: "uniform",
          low: 1,
          high: 3,
        },
      ],
    },
    {
      id: "balanceSheet",
      title: "Balance Sheet & Asset Structure",
      content: [
        {
          id: "cash_and_non_operating_asset",
          label: "Cash and Non-Operating Asset",
          distribution: "uniform",
          low: 1.6,
          high: 1.8,
        },
        {
          id: "asset_liquidation_during_negative_growth",
          label: "Asset Liquidation During Negative Growth",
          distribution: "uniform",
          low: 0,
          high: 0.000000001,
        },
        {
          id: "current_invested_capital",
          label: "Current Invested Capital",
          distribution: "uniform",
          low: 5.8,
          high: 6.2,
        },
        {
          id: "shares_outstanding",
          label: "Shares Outstanding %",
          distribution: "constant",
          value: 0.0275898,
        },
      ],
    },
  ]);

  return (
    <div className="flex flex-col gap-4 w-full p-6 border border-gray-300 rounded-xl backdrop-blur-sm bg-white/80">
      <h2 className="text-2xl font-semibold text-gray-800 text-left">
        Parameters
      </h2>

      <div className="flex flex-col gap-2">
        {sections.map((section) => (
          <div
            key={section.id}
            className="collapse collapse-arrow bg-white/60 border border-gray-300"
          >
            <input
              type="checkbox"
              className="peer"
              checked={expandedSection === section.id}
              onChange={() => toggleSection(section.id)}
            />
            <div className="collapse-title text-lg font-medium text-gray-800">
              {section.title}
            </div>
            <div className="collapse-content">
              <div className="flex flex-col gap-3 pt-2">
                {section.content.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center gap-3 p-3 rounded-lg bg-white/40 hover:bg-white/60 transition-colors cursor-pointer"
                  >
                    <span className="text-gray-700">{item.label}</span>
                    {item.distribution === "triangular" && (
                      <div className="flex w-[300px] gap-2 ml-auto">
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Min"
                          value={item.min}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "min",
                              e.target.value,
                            )
                          }
                        />
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Mode"
                          value={item.mode}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "mode",
                              e.target.value,
                            )
                          }
                        />
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Max"
                          value={item.max}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "max",
                              e.target.value,
                            )
                          }
                        />
                      </div>
                    )}
                    {item.distribution === "skewnorm" && (
                      <div className="flex w-[300px] gap-2 ml-auto">
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Skewness"
                          value={item.skewness}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "skewness",
                              e.target.value,
                            )
                          }
                        />
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Loc"
                          value={item.loc}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "loc",
                              e.target.value,
                            )
                          }
                        />
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Scale"
                          value={item.scale}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "scale",
                              e.target.value,
                            )
                          }
                        />
                      </div>
                    )}
                    {item.distribution === "normal" && (
                      <div className="flex w-[300px] gap-2 ml-auto">
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Mean"
                          value={item.mean}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "mean",
                              e.target.value,
                            )
                          }
                        />
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Std"
                          value={item.std}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "std",
                              e.target.value,
                            )
                          }
                        />
                      </div>
                    )}
                    {item.distribution === "constant" && (
                      <div className="flex w-[300px] gap-2 ml-auto">
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Value"
                          value={item.value}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "value",
                              e.target.value,
                            )
                          }
                        />
                      </div>
                    )}
                    {item.distribution === "uniform" && (
                      <div className="flex w-[300px] gap-2 ml-auto">
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="Low"
                          value={item.low}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "low",
                              e.target.value,
                            )
                          }
                        />
                        <input
                          type="number"
                          className="w-20 flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                          placeholder="High"
                          value={item.high}
                          onChange={(e) =>
                            handleInputChange(
                              section.id,
                              item.id,
                              "high",
                              e.target.value,
                            )
                          }
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DCFForm;
