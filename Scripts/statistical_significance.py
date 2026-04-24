#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistical Significance Testing for Temporal Complexity Trends
Tests whether observed changes from 1943 to 2022 are statistically significant
"""

import json
import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr, mannwhitneyu, ttest_ind
import warnings
warnings.filterwarnings('ignore')

# Load the data
with open('complexity_analysis_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert to arrays by year
years = sorted([int(year) for year in data.keys()])
years_array = np.array(years)

# Features to analyze
features = [
    'word_order_inversion',
    'nominalization',
    'subordination',
    'passive',
    'gerunds_participles',
    'relative_pronouns',
    'appositions',
    'prepositional_phrases',
    'complex_verb_forms'
]

feature_names = {
    'word_order_inversion': 'Word Order Inversion (VS)',
    'nominalization': 'Nominalizations',
    'subordination': 'Subordinate Clauses',
    'passive': 'Passive Constructions',
    'gerunds_participles': 'Gerunds & Participles',
    'relative_pronouns': 'Relative Pronouns & Conjunctions',
    'appositions': 'Appositions & Parentheticals',
    'prepositional_phrases': 'Prepositional Phrases',
    'complex_verb_forms': 'Complex Verb Forms'
}

print("=" * 80)
print("STATISTICAL SIGNIFICANCE TESTING")
print("Temporal Trends in Grammatical Complexity (1943-2022)")
print("=" * 80)
print()

# Extract data for each feature
feature_data = {}
for feature in features:
    values = []
    for year in years:
        year_str = str(year)
        value = data[year_str]['per_sentence'][feature]
        values.append(value)
    feature_data[feature] = np.array(values)

print("1. CORRELATION ANALYSIS (Time vs. Feature Frequency)")
print("-" * 80)
print(f"{'Feature':<40} {'Pearson r':<12} {'p-value':<12} {'Spearman ρ':<12} {'p-value':<12}")
print("-" * 80)

correlation_results = {}

for feature in features:
    values = feature_data[feature]

    # Pearson correlation (assumes linear relationship)
    pearson_r, pearson_p = pearsonr(years_array, values)

    # Spearman correlation (non-parametric, monotonic relationship)
    spearman_rho, spearman_p = spearmanr(years_array, values)

    correlation_results[feature] = {
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_rho': spearman_rho,
        'spearman_p': spearman_p
    }

    name = feature_names[feature]
    print(f"{name:<40} {pearson_r:>11.4f} {pearson_p:>11.4f} {spearman_rho:>11.4f} {spearman_p:>11.4f}")

print()
print("Interpretation:")
print("  r/ρ > 0: Positive correlation (increases over time)")
print("  r/ρ < 0: Negative correlation (decreases over time)")
print("  p < 0.05: Statistically significant at 5% level *")
print("  p < 0.01: Statistically significant at 1% level **")
print("  p < 0.001: Statistically significant at 0.1% level ***")
print()

print("=" * 80)
print()

# Split into periods for comparison
print("2. PERIOD COMPARISON: Early (1943-1960s) vs. Late (2000s-2022)")
print("-" * 80)

early_cutoff = 1970
late_cutoff = 2000

early_years = [y for y in years if y < early_cutoff]
late_years = [y for y in years if y >= late_cutoff]

print(f"Early period: {min(early_years)}-{max(early_years)} (n={len(early_years)} years)")
print(f"Late period:  {min(late_years)}-{max(late_years)} (n={len(late_years)} years)")
print()

print(f"{'Feature':<40} {'Early Mean':<12} {'Late Mean':<12} {'Change %':<12} {'t-stat':<10} {'p-value':<12}")
print("-" * 80)

period_comparison_results = {}

for feature in features:
    values = feature_data[feature]

    early_indices = [i for i, y in enumerate(years) if y < early_cutoff]
    late_indices = [i for i, y in enumerate(years) if y >= late_cutoff]

    early_values = values[early_indices]
    late_values = values[late_indices]

    early_mean = np.mean(early_values)
    late_mean = np.mean(late_values)

    if early_mean > 0:
        change_pct = ((late_mean - early_mean) / early_mean) * 100
    else:
        change_pct = 0

    # Two-sample t-test (parametric)
    t_stat, t_p = ttest_ind(early_values, late_values)

    # Mann-Whitney U test (non-parametric alternative)
    u_stat, u_p = mannwhitneyu(early_values, late_values, alternative='two-sided')

    period_comparison_results[feature] = {
        'early_mean': early_mean,
        'late_mean': late_mean,
        'change_pct': change_pct,
        't_stat': t_stat,
        't_p': t_p,
        'u_stat': u_stat,
        'u_p': u_p
    }

    name = feature_names[feature]
    print(f"{name:<40} {early_mean:>11.3f} {late_mean:>11.3f} {change_pct:>+11.1f}% {t_stat:>9.3f} {t_p:>11.4f}")

print()
print("=" * 80)
print()

# Linear regression analysis
print("3. LINEAR REGRESSION ANALYSIS (Trend Strength)")
print("-" * 80)
print(f"{'Feature':<40} {'Slope':<12} {'R²':<12} {'p-value':<12} {'Trend':<15}")
print("-" * 80)

regression_results = {}

for feature in features:
    values = feature_data[feature]

    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(years_array, values)
    r_squared = r_value ** 2

    # Determine trend direction and significance
    if p_value < 0.001:
        sig = '***'
    elif p_value < 0.01:
        sig = '**'
    elif p_value < 0.05:
        sig = '*'
    else:
        sig = 'n.s.'

    if slope > 0:
        trend = f"Increasing {sig}"
    elif slope < 0:
        trend = f"Decreasing {sig}"
    else:
        trend = f"No trend {sig}"

    regression_results[feature] = {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'p_value': p_value,
        'std_err': std_err
    }

    name = feature_names[feature]
    print(f"{name:<40} {slope:>11.6f} {r_squared:>11.4f} {p_value:>11.4f} {trend:<15}")

print()
print("=" * 80)
print()

# Summary of significant findings
print("4. SUMMARY OF STATISTICALLY SIGNIFICANT TRENDS")
print("-" * 80)
print()

print("SIGNIFICANT INCREASES (p < 0.05):")
print("-" * 40)
increasing = []
for feature in features:
    if regression_results[feature]['slope'] > 0 and regression_results[feature]['p_value'] < 0.05:
        name = feature_names[feature]
        slope = regression_results[feature]['slope']
        p = regression_results[feature]['p_value']
        r2 = regression_results[feature]['r_squared']

        if p < 0.001:
            sig_marker = "***"
        elif p < 0.01:
            sig_marker = "**"
        else:
            sig_marker = "*"

        print(f"  • {name}")
        print(f"    Slope: {slope:.6f} per year")
        print(f"    R² = {r2:.4f}, p = {p:.6f} {sig_marker}")
        print()
        increasing.append(feature)

if not increasing:
    print("  (None)")
    print()

print()
print("SIGNIFICANT DECREASES (p < 0.05):")
print("-" * 40)
decreasing = []
for feature in features:
    if regression_results[feature]['slope'] < 0 and regression_results[feature]['p_value'] < 0.05:
        name = feature_names[feature]
        slope = regression_results[feature]['slope']
        p = regression_results[feature]['p_value']
        r2 = regression_results[feature]['r_squared']

        if p < 0.001:
            sig_marker = "***"
        elif p < 0.01:
            sig_marker = "**"
        else:
            sig_marker = "*"

        print(f"  • {name}")
        print(f"    Slope: {slope:.6f} per year")
        print(f"    R² = {r2:.4f}, p = {p:.6f} {sig_marker}")
        print()
        decreasing.append(feature)

if not decreasing:
    print("  (None)")
    print()

print()
print("NO SIGNIFICANT TREND (p >= 0.05):")
print("-" * 40)
no_trend = []
for feature in features:
    if regression_results[feature]['p_value'] >= 0.05:
        name = feature_names[feature]
        p = regression_results[feature]['p_value']
        print(f"  • {name} (p = {p:.4f})")
        no_trend.append(feature)

if not no_trend:
    print("  (None)")

print()
print("=" * 80)
print()

# Effect sizes
print("5. EFFECT SIZES (Cohen's d for Period Comparison)")
print("-" * 80)
print("{:<40} {:<12} {:<15}".format('Feature', 'Cohen d', 'Effect Size'))
print("-" * 80)

for feature in features:
    values = feature_data[feature]

    early_indices = [i for i, y in enumerate(years) if y < early_cutoff]
    late_indices = [i for i, y in enumerate(years) if y >= late_cutoff]

    early_values = values[early_indices]
    late_values = values[late_indices]

    # Calculate Cohen's d
    pooled_std = np.sqrt(((len(early_values) - 1) * np.var(early_values, ddof=1) +
                          (len(late_values) - 1) * np.var(late_values, ddof=1)) /
                         (len(early_values) + len(late_values) - 2))

    if pooled_std > 0:
        cohens_d = (np.mean(late_values) - np.mean(early_values)) / pooled_std
    else:
        cohens_d = 0

    # Interpret effect size
    abs_d = abs(cohens_d)
    if abs_d < 0.2:
        effect_size = "Negligible"
    elif abs_d < 0.5:
        effect_size = "Small"
    elif abs_d < 0.8:
        effect_size = "Medium"
    else:
        effect_size = "Large"

    name = feature_names[feature]
    print(f"{name:<40} {cohens_d:>11.3f} {effect_size:<15}")

print()
print("Cohen's d interpretation:")
print("  |d| < 0.2: Negligible effect")
print("  |d| < 0.5: Small effect")
print("  |d| < 0.8: Medium effect")
print("  |d| ≥ 0.8: Large effect")
print()

print("=" * 80)
print()

# Save results to JSON
results_summary = {
    'correlation': correlation_results,
    'period_comparison': period_comparison_results,
    'regression': regression_results,
    'significant_increases': [feature_names[f] for f in increasing],
    'significant_decreases': [feature_names[f] for f in decreasing],
    'no_significant_trend': [feature_names[f] for f in no_trend]
}

with open('statistical_significance_results.json', 'w', encoding='utf-8') as f:
    json.dump(results_summary, f, indent=2, ensure_ascii=False)

print("Results saved to: statistical_significance_results.json")
print()
print("✓ Analysis complete!")
