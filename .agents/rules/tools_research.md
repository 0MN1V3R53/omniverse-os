# 🛠️ Tool Affordance Contract: Autonomous Research Pod (`ai_tech_1_rag`)

## Enabled Tools
- `youtube_intel`: Deep video transcript extraction, timestamp segmentation, and technical distillation.
- `web_researcher`: Documentation scraping, API spec extraction, and markdown brief generation.
- `file_system_mcp`: Writing research briefs to `.agents/context/research_briefs/`.

## Activation Triggers
- R&D queries from Executive, Engineering, or Growth pods.
- Technical framework evaluation (e.g. Kotlin Compose Multiplatform, Next.js App Router optimizations).

## Prohibited Actions
- NEVER emit unverified claims without source video/doc attribution.
- NEVER bloat LLM context with raw video transcripts; always virtualize into `.scratchpad/`.
