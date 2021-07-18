import re

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from bs4 import Tag

folder_seasons = Path(__file__).parent.joinpath("raw_layer")

regex_episode_number = re.compile(r"^\d{2}(\d{2})(-\d{2}(\d{2}))?$", re.IGNORECASE)
regex_scene_details = re.compile(r"^\[Scene: (.+)\]$", re.IGNORECASE)
regex_transcription_line = re.compile(r"(\w+): ?(.+)", re.IGNORECASE)


class SceneCategory(Enum):
    BEFORE_OPENING = "before opening"
    MAIN = "main"
    AFTER_CLOSING_CREDITS = "after closing credits"


@dataclass(frozen=True)
class Transcription:
    character: str
    line: str


@dataclass
class Scene:
    category: SceneCategory
    description: Optional[str] = None
    transcriptions: List[Transcription] = field(default_factory=list)


@dataclass(frozen=True)
class Episode:
    number: str
    title: str
    scenes: List[Scene] = field(default_factory=list)


def retrieve_episode_details(season: int, episode: Optional[int] = None) -> Generator[Episode, None, None]:
    # Configure glob pattern
    season_number = str(season).rjust(2, "0")
    episode_number = str(episode).rjust(2, "0") if episode else None
    glob_pattern = f"{season_number}*.html" if not episode_number else f"{season_number}{episode_number}*.html"

    for episode_path in folder_seasons.glob(glob_pattern):
        with open(episode_path.absolute(), mode="r", encoding="iso-8859-1") as episode_file:
            soup = BeautifulSoup(episode_file, "html.parser")
        # Episode's metadata
        match = regex_episode_number.match(episode_path.stem)
        if not match:
            continue
        episodes_groups = match.groups()
        number_1, _, number_2 = episodes_groups
        episode_number = number_1 if number_2 is None else f"{number_1}/{number_2}"
        title = soup.find("title").text
        title = title.split(" - ")[-1]
        episode = Episode(episode_number, title)
        # Let's get all transcription and extract what we need
        scene = Scene(SceneCategory.BEFORE_OPENING)
        scene_category = SceneCategory.BEFORE_OPENING
        all_transcriptions = soup.find_all("p")
        for index, transcription_line in enumerate(all_transcriptions):
            text = transcription_line.text.replace("\n", " ")
            if not text:
                continue
            # As text has content, we can do what we want 👀
            # Basic stuff to define the scene 🎬
            for previous_element in transcription_line.previous_elements:
                if isinstance(previous_element, Tag):
                    text_from_previous = previous_element.text.lower()
                    after_opening = text_from_previous.startswith("opening credits")
                    if after_opening:
                        scene_category = SceneCategory.MAIN
                    after_closing = text_from_previous.startswith("closing credits")
                    if after_closing:
                        scene_category = SceneCategory.AFTER_CLOSING_CREDITS
                    break
            must_create_new_scene = scene.category != scene_category
            if must_create_new_scene:
                episode.scenes.append(scene)
                scene = Scene(scene_category)
            scene_details_line = regex_scene_details.match(text)
            if scene_details_line:
                description = scene_details_line.groups()[0]
                if not scene.description:
                    scene.description = description
                else:
                    episode.scenes.append(scene)
                    scene = Scene(scene_category, description)
                continue
            # If the code is running here, then it will fill up the scene 🎞
            match_character_line = regex_transcription_line.match(text)
            if match_character_line:
                character = match_character_line.groups()[0]
                phrase = match_character_line.groups()[1]
                transcription = Transcription(character.capitalize(), phrase)
                scene.transcriptions.append(transcription)
        # As the last scene is not appended
        episode.scenes.append(scene)
        # The entire defined episode
        yield episode
