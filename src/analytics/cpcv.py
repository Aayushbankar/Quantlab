from itertools import combinations

import numpy as np
import pandas as pd


class CPCV:
    """
    Combinatorial Purged Cross-Validation (CPCV)
    As described by Marcos López de Prado (Advances in Financial Machine Learning, 2018).
    """

    def __init__(self, n_splits: int, n_test_splits: int, embargo_pct: float = 0.01):
        self.n_splits = n_splits
        self.n_test_splits = n_test_splits
        self.embargo_pct = embargo_pct

    def generate_paths(self, timeline_length: int):
        indices = np.arange(timeline_length)
        blocks = np.array_split(indices, self.n_splits)
        test_combinations = list(combinations(range(self.n_splits), self.n_test_splits))
        paths = []

        embargo_size = int(timeline_length * self.embargo_pct)

        for test_blocks in test_combinations:
            test_idx = []
            for i in test_blocks:
                test_idx.extend(blocks[i])

            drop_indices = set(test_idx)
            for i in test_blocks:
                block = blocks[i]
                if len(block) == 0:
                    continue
                start = block[0]
                end = block[-1]

                # Remove embargo_size samples before the test block
                for j in range(max(0, start - embargo_size), start):
                    drop_indices.add(j)
                # Remove embargo_size samples after the test block
                for j in range(end + 1, min(timeline_length, end + 1 + embargo_size)):
                    drop_indices.add(j)

            train_idx = [idx for idx in indices if idx not in drop_indices]
            paths.append((np.array(train_idx), np.array(test_idx)))
        return paths

    def calculate_pbo(self, strategies_returns: pd.DataFrame) -> float:
        """
        Calculates the Probability of Backtest Overfitting (PBO).
        It evaluates the proportion of CPCV paths where the best in-sample strategy
        underperforms the median strategy out-of-sample.
        """
        paths = self.generate_paths(len(strategies_returns))
        if not paths:
            return np.nan

        overfit_count = 0
        valid_paths = 0

        for train_idx, test_idx in paths:
            train_returns = strategies_returns.iloc[train_idx]
            test_returns = strategies_returns.iloc[test_idx]

            # Avoid division by zero by adding a tiny epsilon if std is 0
            train_std = train_returns.std()
            train_std = train_std.replace(0, 1e-8)
            sharpe_is = train_returns.mean() / train_std

            test_std = test_returns.std()
            test_std = test_std.replace(0, 1e-8)
            sharpe_oos = test_returns.mean() / test_std

            # Skip if NaN issues across all strategies
            if sharpe_is.isna().all() or sharpe_oos.isna().all():
                continue

            best_strat = sharpe_is.idxmax()

            oos_perf_of_best_is = sharpe_oos[best_strat]
            median_oos_perf = sharpe_oos.median()

            if pd.isna(oos_perf_of_best_is) or pd.isna(median_oos_perf):
                continue

            if oos_perf_of_best_is < median_oos_perf:
                overfit_count += 1

            valid_paths += 1

        if valid_paths == 0:
            return np.nan

        return overfit_count / valid_paths

    def calculate_pbo_with_ci(
        self,
        strategies_returns: pd.DataFrame,
        n_bootstraps: int = 500,
        ci_level: float = 0.95,
        random_state: int = 42,
    ) -> dict[str, float]:
        """
        Calculates Probability of Backtest Overfitting (PBO) along with
        non-parametric bootstrap confidence intervals across CPCV paths.
        """
        paths = self.generate_paths(len(strategies_returns))
        if not paths:
            return {"pbo": float(np.nan), "ci_lower": float(np.nan), "ci_upper": float(np.nan), "n_paths": 0}

        path_indicators: list[int] = []

        for train_idx, test_idx in paths:
            train_returns = strategies_returns.iloc[train_idx]
            test_returns = strategies_returns.iloc[test_idx]

            train_std = train_returns.std().replace(0, 1e-8)
            sharpe_is = train_returns.mean() / train_std

            test_std = test_returns.std().replace(0, 1e-8)
            sharpe_oos = test_returns.mean() / test_std

            if sharpe_is.isna().all() or sharpe_oos.isna().all():
                continue

            best_strat = sharpe_is.idxmax()
            oos_perf_of_best_is = sharpe_oos[best_strat]
            median_oos_perf = sharpe_oos.median()

            if pd.isna(oos_perf_of_best_is) or pd.isna(median_oos_perf):
                continue

            path_indicators.append(1 if oos_perf_of_best_is < median_oos_perf else 0)

        n_paths = len(path_indicators)
        if n_paths == 0:
            return {"pbo": float(np.nan), "ci_lower": float(np.nan), "ci_upper": float(np.nan), "n_paths": 0}

        pbo = float(np.mean(path_indicators))

        # Bootstrap confidence intervals
        rng = np.random.default_rng(random_state)
        arr = np.array(path_indicators)
        bootstrap_pbos = np.empty(n_bootstraps)
        for b in range(n_bootstraps):
            resample = rng.choice(arr, size=n_paths, replace=True)
            bootstrap_pbos[b] = np.mean(resample)

        alpha = (1.0 - ci_level) / 2.0
        ci_lower = float(np.percentile(bootstrap_pbos, alpha * 100))
        ci_upper = float(np.percentile(bootstrap_pbos, (1.0 - alpha) * 100))

        return {
            "pbo": round(pbo, 4),
            "ci_lower": round(ci_lower, 4),
            "ci_upper": round(ci_upper, 4),
            "n_paths": n_paths,
            "overfit_paths": sum(path_indicators),
        }
