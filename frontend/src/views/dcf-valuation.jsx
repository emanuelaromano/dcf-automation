import { useState, useEffect } from "react";
import axios from "axios";
import { BASE_URL } from "../api";
import StatusBanner from "../components/status-banner";
import { useDispatch, useSelector } from "react-redux";
import {
  setBannerStatusThunk,
  setProcessingStatus,
  setAbortController,
  clearAbortController,
} from "../store/slices/processing";

function DCFValuation() {
  const BASE_COUNTDOWN = 30;
  const [valuation, setValuation] = useState(null);
  const [countdown, setCountdown] = useState(BASE_COUNTDOWN);
  const status = useSelector((state) => state.processing.processingStatus);
  const abortController = useSelector(
    (state) => state.processing.abortController,
  );
  const dispatch = useDispatch();

  useEffect(() => {
    let interval;
    if (status === "generating" && countdown > 0) {
      interval = setInterval(() => {
        setCountdown((prev) => prev - 1);
      }, 1000);
    }
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [status, countdown]);

  // Reset countdown when processing starts
  useEffect(() => {
    if (status === "generating") {
      setCountdown(BASE_COUNTDOWN);
    }
  }, [status]);

  const prepareNumericInput = (values) => {
    const parsed = {};
    for (const key in values) {
      const val = values[key];
      parsed[key] =
        val === "" || isNaN(parseFloat(val)) ? null : parseFloat(val);
    }
    return parsed;
  };

  const initialSections = [
    {
      id: "capitalStructure",
      title: "Capital Structure",
      content: [
        {
          id: "risk_free_rate",
          label: "Risk Free Rate",
          distribution: "normal",
          values: {
            mean: 0.04,
            std: 0.002,
          },
        },
        {
          id: "ERP",
          label: "ERP",
          distribution: "normal",
          values: {
            mean: 0.048,
            std: 0.001,
          },
        },
        {
          id: "equity_value",
          label: "Equity Value",
          distribution: "triangular",
          values: {
            min: 45,
            mode: 51.016,
            max: 57,
          },
        },
        {
          id: "debt_value",
          label: "Debt Value",
          distribution: "triangular",
          values: {
            min: 3.7,
            mode: 3.887,
            max: 4,
          },
        },
        {
          id: "unlevered_beta",
          label: "Unlevered Beta",
          distribution: "triangular",
          values: {
            min: 0.8,
            mode: 0.9,
            max: 1,
          },
        },
        {
          id: "terminal_unlevered_beta",
          label: "Terminal Unlevered Beta",
          distribution: "triangular",
          values: {
            min: 0.8,
            mode: 0.9,
            max: 1,
          },
        },
        {
          id: "year_beta_begins_to_converge_to_terminal_beta",
          label: "Year Beta Begins To Converge To Terminal Beta",
          distribution: "uniform",
          values: {
            low: 1,
            high: 2,
          },
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
          values: {
            min: 0.057,
            mode: 0.06,
            max: 0.063,
          },
        },
        {
          id: "terminal_pretax_cost_of_debt",
          label: "Terminal Pretax Cost Of Debt",
          distribution: "triangular",
          values: {
            min: 0.052,
            mode: 0.055,
            max: 0.058,
          },
        },
        {
          id: "year_cost_of_debt_begins_to_converge_to_terminal_cost_of_debt",
          label: "Year Cost Of Debt Begins To Converge To Terminal Value",
          distribution: "uniform",
          values: {
            low: 1,
            high: 2,
          },
        },
        {
          id: "current_effective_tax_rate",
          label: "Current Effective Tax Rate",
          distribution: "triangular",
          values: {
            min: 0.23,
            mode: 0.24,
            max: 0.25,
          },
        },
        {
          id: "marginal_tax_rate",
          label: "Marginal Tax Rate",
          distribution: "triangular",
          values: {
            min: 0.23,
            mode: 0.25,
            max: 0.27,
          },
        },
        {
          id: "year_effective_tax_rate_begin_to_converge_marginal_tax_rate",
          label: "Year Effective Tax Rate Begin To Converge Marginal Tax Rate",
          distribution: "uniform",
          values: {
            low: 1,
            high: 3,
          },
        },
        {
          id: "additional_return_on_cost_of_capital_in_perpetuity",
          label: "Additional Return On Cost Of Capital In Perpetuity",
          distribution: "triangular",
          values: {
            min: 0.0,
            mode: 0.02,
            max: 0.035,
          },
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
          values: {
            min: 8.8,
            mode: 9.2,
            max: 9.6,
          },
        },
        {
          id: "revenue_growth_rate_cycle1_begin",
          label: "Revenue Growth Rate Cycle 1 Begin",
          distribution: "skewnorm",
          values: {
            skewness: -2.9,
            loc: 0.145,
            scale: 0.032,
          },
        },
        {
          id: "revenue_growth_rate_cycle1_end",
          label: "Revenue Growth Rate Cycle 1 End",
          distribution: "skewnorm",
          values: {
            skewness: -2.9,
            loc: 0.18,
            scale: 0.033,
          },
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
          values: {
            low: 4,
            high: 8,
          },
        },
        {
          id: "revenue_growth_rate_cycle2_begin",
          label: "Revenue Growth Rate Cycle 2 Begin",
          distribution: "skewnorm",
          values: {
            skewness: -2.9,
            loc: 0.165,
            scale: 0.034,
          },
        },
        {
          id: "revenue_growth_rate_cycle2_end",
          label: "Revenue Growth Rate Cycle 2 End",
          distribution: "skewnorm",
          values: {
            skewness: -2.9,
            loc: 0.11,
            scale: 0.032,
          },
        },
        {
          id: "length_of_cycle2",
          label: "Length of Cycle 2",
          distribution: "uniform",
          values: {
            low: 4,
            high: 8,
          },
        },
        {
          id: "revenue_growth_rate_cycle3_begin",
          label: "Revenue Growth Rate Cycle 3 Begin",
          distribution: "skewnorm",
          values: {
            skewness: -2.9,
            loc: 0.09,
            scale: 0.024,
          },
        },
        {
          id: "revenue_growth_rate_cycle3_end",
          label: "Revenue Growth Rate Cycle 3 End",
          distribution: "normal",
          values: {
            mean: 0.04,
            std: 0.002,
          },
        },
        {
          id: "length_of_cycle3",
          label: "Length of Cycle 3",
          distribution: "uniform",
          values: {
            low: 4,
            high: 8,
          },
        },
        {
          id: "revenue_convergance_periods_cycle1",
          label: "Revenue Convergence Periods Cycle 1",
          distribution: "uniform",
          values: {
            low: 1,
            high: 2,
          },
        },
        {
          id: "revenue_convergance_periods_cycle2",
          label: "Revenue Convergence Periods Cycle 2",
          distribution: "uniform",
          values: {
            low: 1,
            high: 2,
          },
        },
        {
          id: "revenue_convergance_periods_cycle3",
          label: "Revenue Convergence Periods Cycle 3",
          distribution: "uniform",
          values: {
            low: 1,
            high: 2,
          },
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
          values: {
            min: 1.5,
            mode: 1.7,
            max: 1.9,
          },
        },
        {
          id: "terminal_sales_to_capital_ratio",
          label: "Terminal Sales to Capital Ratio",
          distribution: "triangular",
          values: {
            min: 1.1,
            mode: 1.3,
            max: 1.6,
          },
        },
        {
          id: "year_sales_to_capital_begins_to_converge_to_terminal_sales_to_capital",
          label: "Year Sales to Capital Begins to Converge to Terminal Value",
          distribution: "uniform",
          values: {
            low: 1,
            high: 3,
          },
        },
        {
          id: "current_operating_margin",
          label: "Current Operating Margin",
          distribution: "triangular",
          values: {
            min: 0.145,
            mode: 0.15,
            max: 0.155,
          },
        },
        {
          id: "terminal_operating_margin",
          label: "Terminal Operating Margin",
          distribution: "triangular",
          values: {
            min: 0.12,
            mode: 0.175,
            max: 0.22,
          },
        },
        {
          id: "year_operating_margin_begins_to_converge_to_terminal_operating_margin",
          label: "Year Operating Margin Begins to Converge to Terminal Value",
          distribution: "uniform",
          values: {
            low: 1,
            high: 3,
          },
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
          values: {
            low: 1.6,
            high: 1.8,
          },
        },
        {
          id: "asset_liquidation_during_negative_growth",
          label: "Asset Liquidation During Negative Growth",
          distribution: "uniform",
          values: {
            low: 0,
            high: 0.000000001,
          },
        },
        {
          id: "current_invested_capital",
          label: "Current Invested Capital",
          distribution: "uniform",
          values: {
            low: 5.8,
            high: 6.2,
          },
        },
        {
          id: "shares_outstanding",
          label: "Shares Outstanding %",
          distribution: "constant",
          values: {
            constant: 0.0275898,
          },
        },
      ],
    },
  ];

  const handleReset = () => {
    setValuation(null);
    setSections(initialSections);
    setCountdown(BASE_COUNTDOWN);
    dispatch(setProcessingStatus("idle"));
    dispatch(clearAbortController());
  };

  const handleInterruptValuation = () => {
    if (abortController) {
      dispatch(setProcessingStatus("cancelling"));
      abortController.abort();
      dispatch(
        setBannerStatusThunk({
          message: "Request cancelled successfully",
          type: "warning",
        }),
      );
      dispatch(setProcessingStatus("cancelled"));
      dispatch(clearAbortController());
    }
  };

  const handleDcfValuationRequest = async () => {
    // Create new AbortController for this request
    const controller = new AbortController();
    dispatch(setAbortController(controller));
    dispatch(setProcessingStatus("generating"));

    const new_sections = [];
    for (const section of sections) {
      for (const item of section.content) {
        new_sections.push({
          id: item.id,
          distribution: item.distribution,
          values: prepareNumericInput(item.values),
        });
      }
    }

    try {
      const response = await axios.post(
        `${BASE_URL}/dcf`,
        {
          input_list: new_sections,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
          signal: controller.signal,
        },
      );

      if (response.status === 200) {
        setValuation(response.data);
        dispatch(
          setBannerStatusThunk({
            message: "Valuation completed successfully!",
            type: "success",
          }),
        );
        dispatch(setProcessingStatus("idle"));
        dispatch(clearAbortController());
      }
    } catch (err) {
      if (err.name === "AbortError" || err.code === "ERR_CANCELED") {
        // Request was cancelled, don't show error message
        dispatch(setProcessingStatus("cancelled"));
        dispatch(clearAbortController());
        return;
      }

      setValuation(null);
      dispatch(
        setBannerStatusThunk({
          message: "Error generating valuation",
          type: "error",
        }),
      );
      dispatch(setProcessingStatus("idle"));
      dispatch(clearAbortController());
    }
  };

  const [expandedSection, setExpandedSection] = useState(null);

  const toggleSection = (section) => {
    if (expandedSection === section) {
      setExpandedSection(null);
    } else {
      setExpandedSection(section);
    }
  };

  const handleInputChange = (sectionId, itemId, field, newValue) => {
    setSections((prevSections) =>
      prevSections.map((section) =>
        section.id === sectionId
          ? {
              ...section,
              content: section.content.map((item) =>
                item.id === itemId
                  ? {
                      ...item,
                      values: {
                        ...item.values,
                        [field]: newValue,
                      },
                    }
                  : item,
              ),
            }
          : section,
      ),
    );
  };

  const [sections, setSections] = useState(initialSections);

  return (
    <div className="flex flex-col w-[900px] z-[1]">
      <StatusBanner />
      <div className="flex flex-col gap-4 w-full mt-20 p-6 border border-gray-300 rounded-xl backdrop-blur-sm bg-white">
        <h2 className="text-2xl font-semibold text-gray-800 text-center">
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Min"
                            value={String(item.values.min ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Mode"
                            value={String(item.values.mode ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Max"
                            value={String(item.values.max ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Skewness"
                            value={String(item.values.skewness ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Loc"
                            value={String(item.values.loc ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Scale"
                            value={String(item.values.scale ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Mean"
                            value={String(item.values.mean ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Std"
                            value={String(item.values.std ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Value"
                            value={String(item.values.constant ?? "")}
                            onChange={(e) =>
                              handleInputChange(
                                section.id,
                                item.id,
                                "constant", // <-- must match the key in `values`
                                e.target.value,
                              )
                            }
                          />
                        </div>
                      )}
                      {item.distribution === "uniform" && (
                        <div className="flex w-[300px] gap-2 ml-auto">
                          <input
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="Low"
                            value={String(item.values.low ?? "")}
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
                            type="text"
                            className="w-20 outline-none flex-1 px-2 py-1 bg-white border border-gray-300 rounded text-gray-800"
                            placeholder="High"
                            value={String(item.values.high ?? "")}
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
      <button
        className={`btn mt-10  ml-10 mr-10 rounded-full generating-btn`}
        onClick={handleDcfValuationRequest}
        disabled={status === "generating" || status === "cancelling"}
      >
        {status === "idle" && "Run DCF Valuation"}
        {status === "generating" && (
          <>
            Running Valuation (estimated {countdown} seconds)
            <svg
              aria-hidden="true"
              role="status"
              className="flex w-4 h-4 text-white animate-spin align-center justify-center"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                className="opacity-25"
              />
              <path
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                className="opacity-75"
              />
            </svg>
          </>
        )}
        {status === "cancelling" && (
          <>
            Cancelling Request...
            <svg
              aria-hidden="true"
              role="status"
              className="flex w-4 h-4 text-white animate-spin align-center justify-center"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                className="opacity-25"
              />
              <path
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                className="opacity-75"
              />
            </svg>
          </>
        )}
        {status === "cancelled" && "Run DCF Valuation"}
      </button>
      {(status === "generating" || status === "cancelling") && (
        <button
          className={`btn mt-2 ml-10 mr-10 rounded-full generating-btn`}
          onClick={handleInterruptValuation}
          disabled={status === "cancelling"}
        >
          {status === "generating" && "Interrupt Valuation"}
          {status === "cancelling" && "Cancelling..."}
        </button>
      )}
      {valuation && <div className="divider"></div>}
      {valuation && (
        <div className="flex justify-center items-center flex-col gap-8">
          <div className="flex flex-col gap-4 p-6 border border-gray-300 rounded-xl backdrop-blur-sm bg-white/80 w-full">
            <div className="grid grid-cols-2 gap-8">
              <div className="flex flex-col">
                <span className="text-sm text-gray-600">
                  Current Market Cap
                </span>
                <span className="text-lg font-medium">
                  {valuation.valuation_summary[0].current_market_cap
                    .toFixed(2)
                    .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                </span>
              </div>
              <div className="flex flex-col">
                <span className="text-sm text-gray-600">
                  Current Price per Share
                </span>
                <span className="text-lg font-medium">
                  {valuation.valuation_summary[0].current_price_per_share
                    .toFixed(2)
                    .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                </span>
              </div>
            </div>
          </div>
          <div className="flex flex-row gap-4 w-full">
            {valuation.valuation_summary.map((summary, index) => (
              <div
                key={index}
                className="flex flex-col w-full p-6 border border-gray-300 rounded-xl backdrop-blur-sm bg-white/80 hover:bg-white/90 transition-all duration-200"
              >
                <div className="text-2xl font-semibold mb-4 text-gray-800">
                  P{summary.percentiles}
                </div>
                <div className="grid gap-4">
                  <div className="flex flex-col">
                    <span className="text-sm text-gray-600">Equity Value</span>
                    <span className="text-lg font-medium">
                      {summary.equity_value
                        .toFixed(2)
                        .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm text-gray-600">
                      Equity Value per Share
                    </span>
                    <span className="text-lg font-medium">
                      {summary.equity_value_per_share
                        .toFixed(2)
                        .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm text-gray-600">Price/Value</span>
                    <span className="text-lg font-medium">
                      {summary["Price/Value"]
                        .toFixed(2)
                        .replace(/\B(?=(\d{3})+(?!\d))/g, ",")}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm text-gray-600">PNL</span>
                    <span className="text-lg font-medium">
                      {summary.PNL.toFixed(2)}%
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="flex flex-col gap-2 w-full">
            {Object.entries(valuation.plots).map(([key, chart], index) => (
              <div key={index} className="w-full overflow-hidden">
                <iframe
                  srcDoc={chart.html
                    .replace(/width:\s*\d+px/g, "width: 100%")
                    .replace(/height:\s*\d+px/g, "height: 600px")}
                  title={key}
                  style={{
                    width: "100%",
                    height: "800px",
                    border: "none",
                    overflow: "hidden",
                  }}
                />
              </div>
            ))}
          </div>
          <button
            className={`btn mt-10 ml-10 mr-10 w-full rounded-full generating-btn`}
            onClick={handleReset}
          >
            Reset
          </button>
        </div>
      )}
    </div>
  );
}

export default DCFValuation;
