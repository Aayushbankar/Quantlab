import { z } from "zod";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export function getApiUrl(path: string): string {
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
}

// -----------------------------------------------------------------------------
// Zod Schemas
// -----------------------------------------------------------------------------

export const StrategyTypeSchema = z.enum([
  "sma_crossover",
  "sma_crossover_10_30",
  "rsi_mean_reversion",
  "momentum",
  "bollinger_breakout",
  "bh_and_hold",
  "buy_and_hold",
]);
export type StrategyType = z.infer<typeof StrategyTypeSchema>;

export const ErrorDetailSchema = z.object({
  code: z.string(),
  message: z.string(),
  details: z.any().optional(),
});
export type ErrorDetail = z.infer<typeof ErrorDetailSchema>;

export const ErrorResponseSchema = z.object({
  error: ErrorDetailSchema,
});
export type ErrorResponse = z.infer<typeof ErrorResponseSchema>;

export const BacktestRequestSchema = z.object({
  strategy: StrategyTypeSchema.default("sma_crossover"),
  params: z.record(z.string(), z.any()).default({}),
  universe: z.array(z.string()).default(["RELIANCE.NS"]),
  start_date: z.string().default("2019-01-01"),
  end_date: z.string().default("2024-12-31"),
  initial_capital: z.number().min(10000).max(100000000).default(100000),
  apply_costs: z.boolean().default(true),
  cost_profile: z.string().default("zerodha_delivery_2024"),
  slippage_floor_bps: z.number().min(0).max(100).default(0.0),
  demo_mode: z.boolean().default(false),
});
export type BacktestRequest = z.infer<typeof BacktestRequestSchema>;

export const CostBreakdownSchema = z.object({
  brokerage: z.number().default(0),
  stt: z.number().default(0),
  stamp_duty: z.number().default(0),
  turnover_fees: z.number().default(0),
  gst: z.number().default(0),
  dp_charges: z.number().default(0),
  sebi_fees: z.number().default(0),
  ipft: z.number().default(0),
  market_impact: z.number().default(0),
  total_friction: z.number().default(0),
  friction_drag_pct: z.number().default(0),
});
export type CostBreakdown = z.infer<typeof CostBreakdownSchema>;

export const TradeRecordSchema = z.object({
  timestamp: z.string(),
  symbol: z.string(),
  side: z.string(),
  quantity: z.number(),
  raw_price: z.number(),
  fill_price: z.number(),
  total_cost: z.number(),
  status: z.string().default("FILLED"),
  reason: z.string().nullable().optional(),
});
export type TradeRecord = z.infer<typeof TradeRecordSchema>;

export const PerformanceMetricsSchema = z.object({
  total_return: z.number(),
  cagr: z.number(),
  sharpe_ratio: z.number(),
  sortino_ratio: z.number(),
  max_drawdown: z.number(),
  calmar_ratio: z.number(),
  average_exposure: z.number().default(0),
  alpha: z.number().default(0),
  beta: z.number().default(0),
  exposure_matched_return: z.number().default(0),
});
export type PerformanceMetrics = z.infer<typeof PerformanceMetricsSchema>;

export const OverfittingDiagnosticsSchema = z.object({
  dsr_p_value: z.number().nullable().optional(),
  expected_max_sharpe: z.number().nullable().optional(),
  pbo: z.number().nullable().optional(),
  pbo_reason: z.string().nullable().optional(),
  n_trials: z.number().default(1),
});
export type OverfittingDiagnostics = z.infer<typeof OverfittingDiagnosticsSchema>;

export const BacktestResponseSchema = z.object({
  run_id: z.string(),
  strategy: z.string(),
  period: z.string().optional(),
  is_cached: z.boolean().default(false),
  served_from: z.enum(["live", "cache", "replay"]).default("live"),
  replay_reason: z.string().nullable().optional(),
  engine_version: z.string().default("1.0.0"),
  data_hash: z.string().default(""),
  cost_profile: z.string().default("standard_discount_2024"),
  execution_time_ms: z.number(),
  dates: z.array(z.string()),
  gross_equity: z.array(z.number()),
  net_equity: z.array(z.number()),
  metrics: PerformanceMetricsSchema,
  costs: CostBreakdownSchema,
  trades: z.array(TradeRecordSchema),
  diagnostics: OverfittingDiagnosticsSchema,
});
export type BacktestResponse = z.infer<typeof BacktestResponseSchema>;

export const StrategyMetadataSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  default_params: z.record(z.string(), z.any()),
  param_ranges: z.record(z.string(), z.any()),
});
export type StrategyMetadata = z.infer<typeof StrategyMetadataSchema>;

export const UniverseResponseSchema = z.object({
  symbols: z.array(z.string()),
  benchmark: z.string(),
  default_start: z.string(),
  default_end: z.string(),
  total_bars: z.number(),
  survivorship_bias_warning: z.string().nullable().optional(),
});
export type UniverseResponse = z.infer<typeof UniverseResponseSchema>;

export const HealthResponseSchema = z.object({
  status: z.string(),
  engine: z.string(),
  version: z.string(),
  cost_model_version: z.string(),
  python_version: z.string(),
  numpy_version: z.string(),
  pandas_version: z.string(),
  demo_mode: z.boolean(),
});
export type HealthResponse = z.infer<typeof HealthResponseSchema>;

export const TrialRecordSchema = z.object({
  trial_id: z.number(),
  strategy: z.string(),
  params: z.record(z.string(), z.any()),
  universe: z.array(z.string()),
  start_date: z.string(),
  end_date: z.string(),
  sharpe: z.number(),
  total_return: z.number(),
  max_drawdown: z.number(),
  run_id: z.string().nullable().optional(),
  created_at: z.string(),
});
export type TrialRecord = z.infer<typeof TrialRecordSchema>;

export const TrialsResponseSchema = z.object({
  total_trials: z.number(),
  trials: z.array(TrialRecordSchema),
  cross_trial_variance: z.number(),
});
export type TrialsResponse = z.infer<typeof TrialsResponseSchema>;

export const SweepSummaryResponseSchema = z.object({
  n_configs_evaluated: z.number(),
  universe_symbols: z.array(z.string()),
  cross_trial_variance: z.number(),
  mean_sharpe: z.number(),
  std_sharpe: z.number(),
  max_sharpe: z.number(),
  min_sharpe: z.number(),
  pbo: z.number().nullable().optional(),
  pbo_ci_lower_95: z.number().nullable().optional(),
  pbo_ci_upper_95: z.number().nullable().optional(),
  cpcv_paths: z.number().default(0),
  cpcv_overfit_paths: z.number().default(0),
  best_config: z.record(z.string(), z.any()).nullable().optional(),
});
export type SweepSummaryResponse = z.infer<typeof SweepSummaryResponseSchema>;

// -----------------------------------------------------------------------------
// Typed API Client Methods
// -----------------------------------------------------------------------------

export class ApiError extends Error {
  code: string;
  details?: unknown;
  status: number;

  constructor(code: string, message: string, status: number, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

async function requestJson<T>(
  endpoint: string,
  options?: RequestInit,
  timeoutMs: number = 30000
): Promise<T> {
  const url = getApiUrl(endpoint);
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
    });

    clearTimeout(id);

    if (!res.ok) {
      let errBody: { error?: { code?: string; message?: string; details?: unknown } } = {};
      try {
        errBody = await res.json();
      } catch {
        errBody = { error: { code: `HTTP_${res.status}`, message: res.statusText } };
      }
      const code = errBody?.error?.code || `HTTP_${res.status}`;
      const msg = errBody?.error?.message || `Request failed with status ${res.status}`;
      throw new ApiError(code, msg, res.status, errBody?.error?.details);
    }

    return (await res.json()) as T;
  } catch (err: unknown) {
    clearTimeout(id);
    if (err instanceof ApiError) throw err;
    if (err instanceof Error && err.name === "AbortError") {
      throw new ApiError("TIMEOUT", `Request to ${endpoint} timed out after ${timeoutMs}ms`, 408);
    }
    const msg = err instanceof Error ? err.message : "Failed to communicate with Pramaan engine";
    throw new ApiError("NETWORK_ERROR", msg, 0);
  }
}

export async function checkHealth(): Promise<HealthResponse> {
  const data = await requestJson<unknown>("/health", { method: "GET" }, 5000);
  return HealthResponseSchema.parse(data);
}

export async function fetchStrategies(): Promise<StrategyMetadata[]> {
  const data = await requestJson<unknown[]>("/strategies", { method: "GET" }, 5000);
  return z.array(StrategyMetadataSchema).parse(data);
}

export async function fetchUniverse(): Promise<UniverseResponse> {
  const data = await requestJson<unknown>("/universe", { method: "GET" }, 5000);
  return UniverseResponseSchema.parse(data);
}

export async function fetchSweepSummary(): Promise<SweepSummaryResponse> {
  const data = await requestJson<unknown>("/sweep", { method: "GET" }, 8000);
  return SweepSummaryResponseSchema.parse(data);
}

export async function fetchTrials(): Promise<TrialsResponse> {
  const data = await requestJson<unknown>("/trials", { method: "GET" }, 8000);
  return TrialsResponseSchema.parse(data);
}

export async function fetchHistory(): Promise<unknown[]> {
  return await requestJson<unknown[]>("/history", { method: "GET" }, 8000);
}

export async function runBacktest(req: BacktestRequest): Promise<BacktestResponse> {
  const data = await requestJson<unknown>("/run", {
    method: "POST",
    body: JSON.stringify(req),
  }, 45000);
  return BacktestResponseSchema.parse(data);
}

export async function submitAsyncJob(req: BacktestRequest): Promise<{ job_id: string; status: string }> {
  return await requestJson<{ job_id: string; status: string }>("/jobs", {
    method: "POST",
    body: JSON.stringify(req),
  }, 10000);
}

export async function pollJob(jobId: string): Promise<{
  job_id: string;
  status: "queued" | "running" | "completed" | "failed";
  progress?: number;
  result?: BacktestResponse;
  error?: string;
}> {
  return await requestJson<{
    job_id: string;
    status: "queued" | "running" | "completed" | "failed";
    progress?: number;
    result?: BacktestResponse;
    error?: string;
  }>(`/jobs/${jobId}`, { method: "GET" }, 10000);
}

export function getReportUrl(runId: string): string {
  return getApiUrl(`/report/${runId}`);
}
