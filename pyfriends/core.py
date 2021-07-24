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

from pyfriends.text_utils import newline_or_nbsp_to_space
from pyfriends.text_utils import strip_left_and_right_sides

folder_seasons = Path(__file__).parent.joinpath("raw_layer")

regex_episode_number = re.compile(r"^\d{2}(\d{2})(-\d{2}(\d{2}))?$", re.IGNORECASE)
regex_scene_details = re.compile(r"^\[Scene: (.+)\]$", re.IGNORECASE)
regex_transcription_line = re.compile(r"(.+?): ?(.+)", re.IGNORECASE)


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
        title = strip_left_and_right_sides(title.split(" - ")[-1])
        episode = Episode(episode_number, title)
        # Let's get all transcription and extract what we need
        scene = Scene(SceneCategory.BEFORE_OPENING)
        all_transcriptions = soup.find_all("p")
        # Some files don't follow the pattern that can be found to the most, so we need to circumvent with a strategy
        can_be_analyzed_normally = len(all_transcriptions) > 10
        all_lines = all_transcriptions
        if not can_be_analyzed_normally:
            all_lines = []
            for transcription_line in all_transcriptions:
                cleared_text = strip_left_and_right_sides(transcription_line.text)
                if "written by" in cleared_text or "end" == cleared_text.lower():
                    continue
                # To keep the same logic during the for loop below 😏
                dirty_lines = cleared_text.split("\n\n")
                for line in dirty_lines:
                    tag_p = soup.new_tag("p")
                    tag_p.string = line
                    all_lines.append(tag_p)
        # If something is wrong, we should know upfront
        generic_error_message = f"episode {episode.number} from {season_number} has to be analysed"
        assert len(all_lines) > 50, f"{generic_error_message}: it has {len(all_lines)} lines"

        for transcription_line in all_lines:
            text = strip_left_and_right_sides(newline_or_nbsp_to_space(transcription_line.text))
            lowercase_text = text.lower()
            disallow_list = ["written by", "transcribed by", "teleplay by"]
            if not text or any(deny_item in lowercase_text for deny_item in disallow_list):
                continue
            # As text has content, we can do what we want 👀
            # Basic stuff to define the scene 🎬
            scene_category = _define_category(transcription_line, text, scene.category)
            must_create_new_scene = scene.category != scene_category
            if must_create_new_scene:
                current_is_before_opening = scene.category == SceneCategory.BEFORE_OPENING
                if current_is_before_opening and len(scene.transcriptions) == 0:
                    scene = Scene(scene_category)
                else:
                    episode.scenes.append(scene)
                    # Sometimes an episode might not have anything before the opening credits
                    # Like episode 1 from season 1 😀
                    if current_is_before_opening and scene_category == SceneCategory.AFTER_CLOSING_CREDITS:
                        for stored_scene in episode.scenes:
                            stored_scene.category = SceneCategory.MAIN
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
                lowercase_character = character.lower()
                invalid_character_case_1 = len(character) > 40
                invalid_character_case_2 = "transcriber" in lowercase_character and "note" in lowercase_character
                if invalid_character_case_1 or invalid_character_case_2:
                    continue
                transcription = Transcription(character.capitalize(), phrase)
                scene.transcriptions.append(transcription)
        # Another sanity check
        assert episode.scenes, f"{generic_error_message}: has no scenes"
        last_included_scene_is_different = episode.scenes[-1] != scene
        scene_has_transcriptions = len(scene.transcriptions) > 0
        scene_after_closing = scene.category == SceneCategory.AFTER_CLOSING_CREDITS
        # Episode 0109 has a scene after closing with no transcriptions
        if last_included_scene_is_different and (scene_has_transcriptions or scene_after_closing):
            episode.scenes.append(scene)
        # The entire defined episode
        yield episode


def _define_category(transcription_line: Tag, text: str, current_category: SceneCategory):
    def retrieve_category_if_possible(text_to_evaluate) -> Optional[SceneCategory]:
        opening_keys = ["opening credits", "opening titles"]
        after_opening = any(key == text_to_evaluate for key in opening_keys)
        if after_opening:
            return SceneCategory.MAIN
        ending_keys = ["ending credits", "closing credits"]
        after_closing = any(key == text_to_evaluate for key in ending_keys)
        if after_closing:
            return SceneCategory.AFTER_CLOSING_CREDITS

    # The tag might have previous elements
    for count, previous_element in enumerate(transcription_line.previous_elements):
        if isinstance(previous_element, Tag):
            lowercase_text = previous_element.text.lower()
            text_from_previous = strip_left_and_right_sides(newline_or_nbsp_to_space(lowercase_text))
            category = retrieve_category_if_possible(text_from_previous)
            if category:
                return category
        # We don't need to traverse all
        if count > 5:
            break

    # If the above wasn't executed, then we can analyse the provided text
    category = retrieve_category_if_possible(text.lower())
    return category if category else current_category
