#!/usr/bin/env python3
"""
OMNIVERSE MASTER WORKFORCE TRAINING SCRIPT: TIMESFM + DEEPSEEK-R1
================================================================
Trains and calibrates all 80+ Omniverse agents with:
1. Google TimesFM 2.5 Time-Series Foundation Model (Zero-Shot Patch Forecasting)
2. DeepSeek-V3 / DeepSeek-R1 Architecture (Multi-Head Latent Attention + DeepSeekMoE + GRPO)
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.models.universal_agent_trainer import UniversalAgentTrainer
from core.models.timesfm_engine import TimesFM25Engine
from core.models.deepseek_frontier_engine import DeepSeekFrontierEngine


def main():
    print("=" * 80)
    print("⚡ OMNIVERSE WORKFORCE TRAINING: GOOGLE TIMESFM 2.5 + DEEPSEEK-R1 ⚡")
    print("=" * 80)

    # 1. Run Universal Agent Training & Matrix Integration
    trainer = UniversalAgentTrainer(workspace_root=_ROOT)
    report = trainer.train_all_agents()

    print("\n" + "=" * 80)
    print(f"🏛️ ENTERPRISE POD CAPABILITY SUMMARY ({report.total_agents_trained} Agents Trained)")
    print("=" * 80)
    
    # Group by Pod
    pod_groups = {}
    for prof in report.all_agent_profiles:
        pod_groups.setdefault(prof.pod_id, []).append(prof)

    for pod_id in sorted(pod_groups.keys(), key=lambda x: int(x.split()[1]) if x.split()[1].isdigit() else 99):
        agents_in_pod = pod_groups[pod_id]
        p_name = agents_in_pod[0].pod_name
        print(f"\n📁 [{pod_id}: {p_name}] ({len(agents_in_pod)} Active Agents)")
        print(f"   • TimesFM Domain:    {agents_in_pod[0].timesfm_domain} ({agents_in_pod[0].timesfm_sample_metric})")
        print(f"   • DeepSeek-R1 Task:   {agents_in_pod[0].deepseek_reasoning_domain}")
        print(f"   • Active Tools:       {', '.join(agents_in_pod[0].active_tools_injected[:3])} (+2 more)")
        for a in agents_in_pod[:3]:
            print(f"     - {a.agent_id} ({a.role_title}) -> TFM Loss: {a.training_loss_timesfm:.4f} | GRPO Reward: {a.grpo_mean_reward:.4f}")
        if len(agents_in_pod) > 3:
            print(f"     - ... and {len(agents_in_pod) - 3} more agents in pod.")

    # 2. Live Diagnostic Forecast: Google Ads Spend Pacing (Pod 20)
    print("\n" + "=" * 80)
    print("📈 LIVE DIAGNOSTIC 1: GOOGLE ADS SPEND PACING FORECAST (TIMESFM 2.5)")
    print("=" * 80)
    tfm = TimesFM25Engine()
    historical_ads_spend = [28.5, 27.8, 28.2, 28.5, 28.1, 28.4, 28.5, 28.3, 28.5, 28.2, 28.5, 28.4, 28.5, 28.5]
    ads_forecast = tfm.forecast(
        historical_values=historical_ads_spend,
        horizon=7,
        domain="daily_budget_pacing_and_impr_velocity",
        series_id="PMAX-CAMPAIGN-1-SPEND"
    )
    print(f"Series ID:          {ads_forecast.series_id}")
    print(f"Model:              {ads_forecast.model_version} (Latency: {ads_forecast.execution_latency_ms} ms)")
    print(f"Next 7 Days Mean:   {ads_forecast.point_forecast}")
    print(f"10th Quantile (q10):{ads_forecast.quantile_forecasts['q10']}")
    print(f"90th Quantile (q90):{ads_forecast.quantile_forecasts['q90']}")
    print(f"MAE Estimate:       ${ads_forecast.mean_absolute_error_estimate:.4f}")

    # 3. Live Diagnostic Forecast: SEO Googlebot Crawl Velocity (Pod 4)
    print("\n" + "=" * 80)
    print("🔍 LIVE DIAGNOSTIC 2: SEO GOOGLEBOT CRAWL VELOCITY (TIMESFM 2.5)")
    print("=" * 80)
    historical_crawl = [142, 165, 189, 210, 245, 280, 310, 345, 390, 420, 460, 510, 580, 640]
    seo_forecast = tfm.forecast(
        historical_values=historical_crawl,
        horizon=7,
        domain="serp_rank_and_crawl_velocity",
        series_id="SKY-SEO-3148-CORRIDORS"
    )
    print(f"Series ID:          {seo_forecast.series_id}")
    print(f"Next 7 Days Mean:   {seo_forecast.point_forecast} req/hr")
    print(f"80% Conf Bounds:    {seo_forecast.confidence_interval_80[:3]} ...")

    # 4. Live Diagnostic GRPO Reasoning: DeepSeek-R1 Architecture
    print("\n" + "=" * 80)
    print("🧠 LIVE DIAGNOSTIC 3: DEEPSEEK-R1 GRPO REASONING & MOE ROUTING")
    print("=" * 80)
    r1 = DeepSeekFrontierEngine()
    grpo_run = r1.execute_grpo_reasoning(
        prompt="Synthesize zero-drift Performance Max negative keyword shield and TimesFM quote bid calibration.",
        domain="smart_bidding_auction_defense",
        group_size=4
    )
    print(f"Architecture:       {grpo_run.architecture} (Latency: {grpo_run.execution_latency_ms} ms)")
    print(f"Group Size (G):     {grpo_run.group_size} Streams Evaluated")
    print(f"Mean Group Reward:  {grpo_run.mean_group_reward:.4f} (Std: {grpo_run.reward_std_dev:.4f})")
    print(f"GRPO Loss Est:      {grpo_run.grpo_loss_estimate:.6f}")
    print(f"Selected Stream ID: {grpo_run.selected_stream.stream_id} (Reward: {grpo_run.selected_stream.reward_score:.4f}, Advantage: {grpo_run.selected_stream.relative_advantage})")
    print(f"Step PRM Scores:    {grpo_run.selected_stream.step_scores}")
    print(f"Thought Preview:\n{grpo_run.selected_stream.thought_process[:250]}...\n</think>")

    print("\n" + "=" * 80)
    print(f"💾 Workforce Capability Matrix Persisted to: {report.matrix_export_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
