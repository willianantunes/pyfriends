from unittest import TestCase

from pyfriends.core import SceneCategory
from pyfriends.core import retrieve_episode_details


class Test(TestCase):
    def test_retrieve_episode_details_from_0107(self):
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
