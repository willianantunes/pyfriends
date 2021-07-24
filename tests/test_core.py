from typing import Union
from unittest import TestCase

from pyfriends.core import Episode
from pyfriends.core import Scene
from pyfriends.core import SceneCategory
from pyfriends.core import retrieve_episode_details

allow_list_may_have_zero_transcription = [(1, "03"), (1, "09"), (4, "21"), (5, "23"), (9, "09"), (4, "02"), (6, "24")]


class AllSeasons(TestCase):
    def test_general_assertions_to_cover(self):
        seasons_identifiers = range(1, 11)

        for season_identifier in seasons_identifiers:
            episodes = retrieve_episode_details(season_identifier)
            for episode in episodes:
                error_message = f"Episode {episode.number} from season {season_identifier}"
                assert episode.title, error_message
                assert episode.number, error_message
                # At least 4 scenes per episode
                number_of_scenes = len(episode.scenes)
                assert number_of_scenes >= 4, f"{error_message} has only {number_of_scenes} scenes"
                for scene in episode.scenes:
                    # Each scene must have all of its properties defined
                    assert scene.category, error_message
                    assert scene.description, f"{error_message} with category {scene.category}"
                    number_of_transcriptions = len(scene.transcriptions)
                    transcription_assertion = (
                        number_of_transcriptions >= 1
                        or (season_identifier, episode.number) in allow_list_may_have_zero_transcription
                    )
                    assert (
                        transcription_assertion
                    ), f"{error_message} has {number_of_transcriptions} transcription in scene: {scene.description}"
                    for transcription in scene.transcriptions:
                        # Each transcription must have all of its properties defined
                        assert transcription.character, error_message
                        assert transcription.line, error_message


class CustomTestCase(TestCase):
    def general_episode_validation(
        self,
        episode: Episode,
        expected_episode_title: str,
        expected_episode_number: Union[str, int],
        expected_total_scenes: int,
        expected_scenes_before_opening: int,
        expected_scenes_main: int,
        expected_scenes_after_main: int,
    ):
        expected_episode_number = (
            expected_episode_number
            if type(expected_episode_number) is str
            else str(expected_episode_number).rjust(2, "0")
        )
        self.assertEqual(str(expected_episode_number), episode.number)
        self.assertEqual(expected_episode_title, episode.title)
        self.assertEqual(expected_total_scenes, len(episode.scenes))
        scenes_before_opening = [scene for scene in episode.scenes if scene.category == SceneCategory.BEFORE_OPENING]
        scenes_main = [scene for scene in episode.scenes if scene.category == SceneCategory.MAIN]
        scenes_after_main = [scene for scene in episode.scenes if scene.category == SceneCategory.AFTER_CLOSING_CREDITS]
        self.assertTrue(
            expected_total_scenes == (len(scenes_before_opening) + len(scenes_main) + len(scenes_after_main))
        )
        for scene in episode.scenes:
            self.assertIsNotNone(scene.category)
            self.assertIsNotNone(scene.description, f"error from category {scene.category}")
            self.evaluate_transcriptions(episode.title, scene)
        # Evaluating before OPENING
        self.assertEqual(expected_scenes_before_opening, len(scenes_before_opening))
        # Evaluating after OPENING (which is category MAIN)
        self.assertEqual(expected_scenes_main, len(scenes_main))
        # Evaluating after CLOSING CREDITS
        self.assertEqual(expected_scenes_after_main, len(scenes_after_main))

    def evaluate_transcriptions(self, episode_title: str, scene: Scene):
        number_of_transcriptions = len(scene.transcriptions)
        has_valid_number_of_transcription = number_of_transcriptions >= 1
        error_message = f"{number_of_transcriptions} in scene {scene.description}"
        is_allowed = False
        if not has_valid_number_of_transcription:
            allowed_episodes = [
                "The One With The Thumb",
                "The One Where Underdog Gets Away",
                "The One In Vegas",
                "The One With Rachel's Phone Number",
                "The One With The Proposal",
            ]
            final_allow_list = allowed_episodes
            is_allowed = episode_title in final_allow_list
        self.assertTrue(has_valid_number_of_transcription or is_allowed, error_message)


class FirstSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_7(self):
        # Arrange
        season = 1
        episode_number = 7
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        self.assertEqual(episode_number, int(episode.number))
        self.assertEqual("The One With the Blackout", episode.title)
        total_scenes = 21
        self.assertEqual(total_scenes, len(episode.scenes))
        scenes_before_opening = [scene for scene in episode.scenes if scene.category == SceneCategory.BEFORE_OPENING]
        scenes_main = [scene for scene in episode.scenes if scene.category == SceneCategory.MAIN]
        scenes_after_main = [scene for scene in episode.scenes if scene.category == SceneCategory.AFTER_CLOSING_CREDITS]
        self.assertTrue(total_scenes == (len(scenes_before_opening) + len(scenes_main) + len(scenes_after_main)))
        # Evaluating before OPENING
        self.assertEqual(2, len(scenes_before_opening))
        before_opening_scene_1 = scenes_before_opening[0]
        self.assertEqual(
            "Central Perk, Rachel is introducing Phoebe, who is playing her guitar for the crowd.",
            before_opening_scene_1.description,
        )
        self.assertEqual(2, len(before_opening_scene_1.transcriptions))
        before_opening_scene_2 = scenes_before_opening[1]
        self.assertEqual(
            "The ATM vestibule of a bank, Chandler is inside. The lights go out, and he realizes he is trapped inside.",
            before_opening_scene_2.description,
        )
        self.assertEqual(1, len(before_opening_scene_2.transcriptions))
        # Evaluating after OPENING (which is category MAIN)
        self.assertEqual(18, len(scenes_main))
        # Evaluating after CLOSING CREDITS
        self.assertEqual(1, len(scenes_after_main))
        last_scene = scenes_after_main[0]
        self.assertEqual(4, len(last_scene.transcriptions))
        self.assertEqual(2, len(list(filter(lambda t: t.character == "Jill", last_scene.transcriptions))))
        self.assertEqual(2, len(list(filter(lambda t: t.character == "Chandler", last_scene.transcriptions))))

    def test_retrieve_episode_details_from_episode_3(self):
        # Arrange
        season = 1
        episode_number = 3
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With The Thumb"
        expected_episode_number = episode_number
        expected_total_scenes = 15
        expected_scenes_before_opening = 1
        expected_scenes_main = 13
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_8(self):
        # Arrange
        season = 1
        episode_number = 8
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Nana Dies Twice"
        expected_episode_number = episode_number
        expected_total_scenes = 13
        expected_scenes_before_opening = 1
        expected_scenes_main = 11
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_22(self):
        # Arrange
        season = 1
        episode_number = 22
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With The Ick Factor"
        expected_episode_number = episode_number
        expected_total_scenes = 13
        expected_scenes_before_opening = 1
        expected_scenes_main = 11
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_17(self):
        # Arrange
        season = 1
        episode_number = 17
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With Two Parts, Part 2"
        expected_episode_number = episode_number
        expected_total_scenes = 14
        expected_scenes_before_opening = 0
        expected_scenes_main = 13
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_9(self):
        # Arrange
        season = 1
        episode_number = 9
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Underdog Gets Away"
        expected_episode_number = episode_number
        expected_total_scenes = 13
        expected_scenes_before_opening = 1
        expected_scenes_main = 11
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_1(self):
        # Arrange
        season = 1
        episode_number = 1
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Monica Gets a New Roommate"
        expected_episode_number = episode_number
        expected_total_scenes = 15
        expected_scenes_before_opening = 0
        expected_scenes_main = 14
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_14(self):
        # Arrange
        season = 1
        episode_number = 14
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With the Candy Hearts"
        expected_episode_number = episode_number
        expected_total_scenes = 17
        expected_scenes_before_opening = 1
        expected_scenes_main = 14
        expected_scenes_after_main = 2
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )


class SecondSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_14(self):
        # Arrange
        season = 2
        episode_number = 14
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With the Prom Video"
        expected_episode_number = episode_number
        expected_total_scenes = 11
        expected_scenes_before_opening = 1
        expected_scenes_main = 9
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_15(self):
        # Arrange
        season = 2
        episode_number = 15
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Ross and Rachel...You Know"
        expected_episode_number = episode_number
        expected_total_scenes = 15
        expected_scenes_before_opening = 1
        expected_scenes_main = 13
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_11(self):
        # Arrange
        season = 2
        episode_number = 11
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With the Lesbian Wedding"
        expected_episode_number = episode_number
        expected_total_scenes = 15
        expected_scenes_before_opening = 1
        expected_scenes_main = 13
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_16(self):
        # Arrange
        season = 2
        episode_number = 16
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Joey Moves Out"
        expected_episode_number = episode_number
        expected_total_scenes = 16
        expected_scenes_before_opening = 1
        expected_scenes_main = 15
        expected_scenes_after_main = 0
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )


class FifthSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_23(self):
        # Arrange
        season = 5
        episode_number = 23
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One In Vegas"
        expected_episode_number = episode_number
        expected_total_scenes = 28
        expected_scenes_before_opening = 1
        expected_scenes_main = 27
        expected_scenes_after_main = 0
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )


class SixthSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_24(self):
        # Arrange
        season = 6
        episode_number = 24
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With The Proposal"
        expected_episode_number = episode_number
        expected_total_scenes = 28
        expected_scenes_before_opening = 1
        expected_scenes_main = 26
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )


class SeventhSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_23(self):
        # Arrange
        season = 7
        episode_number = 23
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With Chandler and Monica's Wedding"
        expected_episode_number = episode_number
        expected_total_scenes = 26
        expected_scenes_before_opening = 1
        expected_scenes_main = 25
        expected_scenes_after_main = 0
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )


class NinthSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_9(self):
        # Arrange
        season = 9
        episode_number = 9
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With Rachel's Phone Number"
        expected_episode_number = episode_number
        expected_total_scenes = 14
        expected_scenes_before_opening = 1
        expected_scenes_main = 12
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_11(self):
        # Arrange
        season = 9
        episode_number = 11
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Rachel Goes Back To Work"
        expected_episode_number = episode_number
        expected_total_scenes = 17
        expected_scenes_before_opening = 1
        expected_scenes_main = 15
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )


class TenthSeason(CustomTestCase):
    def test_retrieve_episode_details_from_episode_17(self):
        # Arrange
        season = 10
        episode_number = 17
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The Last One"
        expected_episode_number = "17/18"
        expected_total_scenes = 25
        expected_scenes_before_opening = 2
        expected_scenes_main = 23
        expected_scenes_after_main = 0
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_4(self):
        # Arrange
        season = 10
        episode_number = 4
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One With The Cake"
        expected_episode_number = 4
        expected_total_scenes = 6
        expected_scenes_before_opening = 1
        expected_scenes_main = 4
        expected_scenes_after_main = 1
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )

    def test_retrieve_episode_details_from_episode_10(self):
        # Arrange
        season = 10
        episode_number = 10
        # Act
        episodes = list(retrieve_episode_details(season, episode_number))
        # Assert
        self.assertEqual(1, len(episodes))
        episode = episodes[0]
        expected_episode_title = "The One Where Chandler Gets Caught"
        expected_episode_number = episode_number
        expected_total_scenes = 7
        expected_scenes_before_opening = 1
        expected_scenes_main = 6
        expected_scenes_after_main = 0
        self.general_episode_validation(
            episode,
            expected_episode_title,
            expected_episode_number,
            expected_total_scenes,
            expected_scenes_before_opening,
            expected_scenes_main,
            expected_scenes_after_main,
        )
