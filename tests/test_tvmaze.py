from datetime import date
from unittest import TestCase

from pyfriends.tvmaze import Cast
from pyfriends.tvmaze import Character
from pyfriends.tvmaze import Episode
from pyfriends.tvmaze import Network
from pyfriends.tvmaze import Person
from pyfriends.tvmaze import Season
from pyfriends.tvmaze import Show
from pyfriends.tvmaze import all_episodes
from pyfriends.tvmaze import all_seasons
from pyfriends.tvmaze import episode_details
from pyfriends.tvmaze import main_cast
from pyfriends.tvmaze import show_details


class TestTVMaze(TestCase):
    def test_should_retrieve_show_details_about_friends(self):
        # Arrange
        friends_id = 431
        # Act
        show = show_details(friends_id)
        # Assert
        expected_object = Show(
            name="Friends",
            genres=["Comedy", "Romance"],
            premiered=date(1994, 9, 22),
            summary="Six young (20-something) people from New York City (Manhattan), on their own and struggling to "
            "survive in the real world, find the companionship, comfort and support they get from each other "
            "to be the perfect antidote to the pressures of life.This average group of buddies goes through "
            "massive mayhem, family trouble, past and future romances, fights, laughs, tears and surprises as "
            "they learn what it really means to be a friend.",
            network=Network(name="NBC", country="United States"),
        )
        self.assertEqual(expected_object, show)

    def test_should_retrieve_nothing_given_id_is_invalid(self):
        # Arrange
        fake_id = -10
        # Act
        show = show_details(fake_id)
        # Assert
        self.assertIsNone(show)

    def test_should_retrieve_season_1_episode_1_details_from_friends(self):
        # Arrange
        friends_id = 431
        season_number = 1
        episode_number = 1
        # Act
        show = episode_details(friends_id, season_number, episode_number)
        # Assert
        expected_object = Episode(
            title="The One Where Monica Gets a Roommate",
            air_date=date(1994, 9, 22),
            runtime=30,
            summary="Monica's old friend Rachel moves in with her after leaving her fiancé.",
            type="regular",
        )
        self.assertEqual(expected_object, show)

    def test_should_retrieve_all_seasons_from_friends(self):
        # Arrange
        friends_id = 431
        # Act
        seasons = all_seasons(friends_id)
        # Assert
        expected_list = [
            Season(
                id=1716, number=1, number_of_episodes=24, premiered_date=date(1994, 9, 22), end_date=date(1995, 5, 18)
            ),
            Season(
                id=1717, number=2, number_of_episodes=24, premiered_date=date(1995, 9, 21), end_date=date(1996, 5, 16)
            ),
            Season(
                id=1718, number=3, number_of_episodes=25, premiered_date=date(1996, 9, 16), end_date=date(1997, 5, 15)
            ),
            Season(
                id=1719, number=4, number_of_episodes=24, premiered_date=date(1997, 9, 25), end_date=date(1998, 5, 7)
            ),
            Season(
                id=1720, number=5, number_of_episodes=24, premiered_date=date(1998, 9, 24), end_date=date(1999, 5, 20)
            ),
            Season(
                id=1721, number=6, number_of_episodes=25, premiered_date=date(1999, 9, 23), end_date=date(2000, 5, 18)
            ),
            Season(
                id=1722, number=7, number_of_episodes=24, premiered_date=date(2000, 10, 12), end_date=date(2001, 5, 17)
            ),
            Season(
                id=1723, number=8, number_of_episodes=24, premiered_date=date(2001, 9, 27), end_date=date(2002, 5, 16)
            ),
            Season(
                id=1724, number=9, number_of_episodes=24, premiered_date=date(2002, 9, 26), end_date=date(2003, 5, 15)
            ),
            Season(
                id=1725, number=10, number_of_episodes=18, premiered_date=date(2003, 9, 25), end_date=date(2004, 5, 6)
            ),
        ]
        self.assertEqual(expected_list, seasons)

    def test_should_retrieve_all_episodes_given_1st_season_friends(self):
        # Arrange
        first_season_id = 1716
        # Act
        episodes = all_episodes(first_season_id)
        # Assert
        expected_list = [
            Episode(
                title="The One Where Monica Gets a Roommate",
                air_date=date(1994, 9, 22),
                runtime=30,
                summary="Monica's old friend Rachel moves in with her after leaving her fiancé.",
                type="regular",
            ),
            Episode(
                title="The One With the Sonogram at the End",
                air_date=date(1994, 9, 29),
                runtime=30,
                summary="Rachel returns her engagement ring; Ross's ex-wife has a revelation for him.",
                type="regular",
            ),
            Episode(
                title="The One With the Thumb",
                air_date=date(1994, 10, 6),
                runtime=30,
                summary="Monica's friends find her new beau appealing; Phoebe finds a little something extra in her soda.",
                type="regular",
            ),
            Episode(
                title="The One With George Stephanopoulos",
                air_date=date(1994, 10, 13),
                runtime=30,
                summary="Chandler and Joey take Ross to a hockey game -- with painful results; the ladies get someone else's pizza.",
                type="regular",
            ),
            Episode(
                title="The One With the East German Laundry Detergent",
                air_date=date(1994, 10, 20),
                runtime=30,
                summary="Ross does laundry with Rachel; Joey uses Monica to get his old girlfriend back.",
                type="regular",
            ),
            Episode(
                title="The One With the Butt",
                air_date=date(1994, 10, 27),
                runtime=30,
                summary="Joey's new agent gets him a cheeky role in a movie; Chandler dates a woman with lots of baggage.",
                type="regular",
            ),
            Episode(
                title="The One With the Blackout",
                air_date=date(1994, 11, 3),
                runtime=30,
                summary="A blackout traps Chandler in an ATM vestibule with model Jill Goodacre; a cat comes between Ross and Rachel.",
                type="regular",
            ),
            Episode(
                title="The One Where Nana Dies Twice",
                air_date=date(1994, 11, 10),
                runtime=30,
                summary="Monica and Ross mourn the loss of their grandmother.",
                type="regular",
            ),
            Episode(
                title="The One Where Underdog Gets Away",
                air_date=date(1994, 11, 17),
                runtime=30,
                summary="Monica tries to cook Thanksgiving dinner for the gang; Ross relishes the chance to talk to his unborn child.",
                type="regular",
            ),
            Episode(
                title="The One With the Monkey",
                air_date=date(1994, 12, 15),
                runtime=30,
                summary="A new pet monkeys around with Ross's ego during the holidays; Phoebe falls for a scientist .",
                type="regular",
            ),
            Episode(
                title="The One With Mrs. Bing",
                air_date=date(1995, 1, 5),
                runtime=30,
                summary="Chandler's novelist mother visits -- and hits on Ross; Phoebe and Monica fall for the same guy.",
                type="regular",
            ),
            Episode(
                title="The One With the Dozen Lasagnas",
                air_date=date(1995, 1, 12),
                runtime=30,
                summary="Phoebe has some bad news for Rachel about Paolo; Ross learns some of the results of his former wife's amniocentesis.",
                type="regular",
            ),
            Episode(
                title="The One With the Boobies",
                air_date=date(1995, 1, 19),
                runtime=30,
                summary="Chandler sees Rachel naked; Joey learns his father is having an affair; Phoebe dates a psychiatrist.",
                type="regular",
            ),
            Episode(
                title="The One With the Candy Hearts",
                air_date=date(1995, 2, 9),
                runtime=30,
                summary="Chandler has a blind date with an ex-girlfriend -- whom he's broken up with twice before; the ladies light a \"boyfriend bonfire\"; Ross finds an unlikely Valentine's Day date.",
                type="regular",
            ),
            Episode(
                title="The One With the Stoned Guy",
                air_date=date(1995, 2, 16),
                runtime=30,
                summary="Chandler and Monica plan big career moves, while Ross labors to hit it off with a date.",
                type="regular",
            ),
            Episode(
                title="The One With Two Parts, Part 1",
                air_date=date(1995, 2, 23),
                runtime=30,
                summary="Ross attends Lamaze classes; Joey dates Phoebe's twin; and Chandler has the hots for a co-worker he's supposed to fire.",
                type="regular",
            ),
            Episode(
                title="The One With Two Parts, Part 2",
                air_date=date(1995, 2, 23),
                runtime=30,
                summary="Monica and Rachel meet two cute doctors; Ross looks to Jack for fatherly advice; Phoebe confronts her twin about Joey.",
                type="regular",
            ),
            Episode(
                title="The One With All the Poker",
                air_date=date(1995, 3, 2),
                runtime=30,
                summary="The guys let the ladies in on a sacred ritual -- their poker game. Meanwhile, Rachel has an interview with Saks.",
                type="regular",
            ),
            Episode(
                title="The One Where the Monkey Gets Away",
                air_date=date(1995, 3, 9),
                runtime=30,
                summary="Ross entrusts Rachel with his pet monkey for a day; Barry has a surprise for Rachel.",
                type="regular",
            ),
            Episode(
                title="The One With the Evil Orthodontist",
                air_date=date(1995, 4, 6),
                runtime=30,
                summary="Chandler's not a very smooth operator when it comes to calling a woman he went out with; Rachel gets involved with her ex-fiancé.",
                type="regular",
            ),
            Episode(
                title="The One With the Fake Monica",
                air_date=date(1995, 4, 27),
                runtime=30,
                summary="Monica meets the woman who used her credit-card number; Ross realizes it's time to find a new home for Marcel.",
                type="regular",
            ),
            Episode(
                title="The One With the Ick Factor",
                air_date=date(1995, 5, 4),
                runtime=30,
                summary="Phoebe gets temporary work as Chandler's secretary; Monica's new boyfriend is younger than she thinks.",
                type="regular",
            ),
            Episode(
                title="The One With the Birth",
                air_date=date(1995, 5, 11),
                runtime=30,
                summary="Ross quarrels with Susan in the delivery room as Carol prepares to give birth; Joey befriends a mother-to-be.",
                type="regular",
            ),
            Episode(
                title="The One Where Rachel Finds Out",
                air_date=date(1995, 5, 18),
                runtime=30,
                summary="Rachel finally realizes how much Ross likes her -- but not before he leaves for China on museum business.",
                type="regular",
            ),
        ]
        self.assertEqual(expected_list, episodes)

    def test_should_retrieve_main_cast_about_friends(self):
        # Arrange
        friend_id = 431
        # Act
        main_characters = main_cast(friend_id)
        # Assert
        expected_list = [
            Cast(
                character=Character(id=78218, name="Rachel Green"),
                person=Person(
                    id=24483,
                    name="Jennifer Aniston",
                    country="United States",
                    birthday=date(1969, 2, 11),
                    gender="Female",
                ),
            ),
            Cast(
                character=Character(id=78219, name="Monica Geller"),
                person=Person(
                    id=36167, name="Courteney Cox", country="United States", birthday=date(1964, 6, 15), gender="Female"
                ),
            ),
            Cast(
                character=Character(id=78220, name="Phoebe Buffay"),
                person=Person(
                    id=17185, name="Lisa Kudrow", country="United States", birthday=date(1963, 7, 30), gender="Female"
                ),
            ),
            Cast(
                character=Character(id=78221, name="Joey Tribbiani"),
                person=Person(
                    id=27937, name="Matt LeBlanc", country="United States", birthday=date(1967, 7, 25), gender="Male"
                ),
            ),
            Cast(
                character=Character(id=78222, name="Chandler Bing"),
                person=Person(
                    id=20532, name="Matthew Perry", country="United States", birthday=date(1969, 8, 19), gender="Male"
                ),
            ),
            Cast(
                character=Character(id=78223, name="Ross Geller"),
                person=Person(
                    id=45515, name="David Schwimmer", country="United States", birthday=date(1966, 11, 2), gender="Male"
                ),
            ),
        ]
        self.assertEqual(expected_list, main_characters)
