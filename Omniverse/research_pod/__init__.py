"""
Autonomous Research Pod Package.
Provides YouTube video transcript extraction, live web intelligence, and automated research dossiers.
"""

from .youtube_crawler import YouTubeIntelCrawler, VideoTranscriptBrief
from .web_crawler import WebIntelCrawler, WebArticleBrief
from .researcher import AutonomousResearchPod, ResearchDossier

__all__ = [
    "YouTubeIntelCrawler",
    "VideoTranscriptBrief",
    "WebIntelCrawler",
    "WebArticleBrief",
    "AutonomousResearchPod",
    "ResearchDossier",
]
