"""
-- Dataclasses in project --

:YouTubeVideo
"""
import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class YouTubeVideo:
    """ 
    Youtube video container 
    """
    video_id: str
    title: str
    description: str
    length_text: str
    url: str
    tumbnail_url: str
