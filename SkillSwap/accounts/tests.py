from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile
from skills.models import Skill, OfferedSkill, NeededSkill

class UserProfileTestCase(TestCase):
    """
    Test suite to check UserProfile, offered skills, and needed skills
    """

    def setUp(self):
        print("\n" + "="*60)
        print("Setting up test data for UserProfile...")
        print("="*60)

        # Users
        self.user_ali = User.objects.create_user(username='ali', password='12345')
        self.user_mary = User.objects.create_user(username='mary', password='12345')

        # Profiles
        self.profile_ali = UserProfile.objects.create(user=self.user_ali, bio='Hi I am Ali')
        self.profile_mary = UserProfile.objects.create(user=self.user_mary, bio='Hi I am Mary')

        # Skills
        self.skill_python = Skill.objects.create(skill='Python')
        self.skill_django = Skill.objects.create(skill='Django')

        # Offered skills
        self.offer_ali = OfferedSkill.objects.create(
            user=self.user_ali, skill=self.skill_python, description='Python programming', hourly_rate_equivalent=30
        )
        self.offer_mary = OfferedSkill.objects.create(
            user=self.user_mary, skill=self.skill_django, description='Django framework', hourly_rate_equivalent=40
        )

        # Needed skills
        self.need_ali = NeededSkill.objects.create(
            user=self.user_ali, skill=self.skill_django, description='Need Django help', urgency='high'
        )
        self.need_mary = NeededSkill.objects.create(
            user=self.user_mary, skill=self.skill_python, description='Need Python help', urgency='medium'
        )

        print("✓ Test data setup complete!\n")

    def test_profile_offered_skills(self):
        print("\nChecking offered skills for Ali...")
        offered = self.profile_ali.offered_skills()
        for off in offered:
            print(f"{self.profile_ali.user.username} offers {off.skill.skill} at ${off.hourly_rate_equivalent}/hr")
        self.assertEqual(offered.count(), 1)

    def test_profile_needed_skills(self):
        print("\nChecking needed skills for Ali...")
        needed = self.profile_ali.needed_skills()
        for need in needed:
            print(f"{self.profile_ali.user.username} needs {need.skill.skill} ({need.urgency})")
        self.assertEqual(needed.count(), 1)

    def test_profile_links(self):
        print("\nChecking profile-user links...")
        self.assertEqual(self.profile_ali.user.username, 'ali')
        self.assertEqual(self.profile_mary.user.username, 'mary')
        print("✓ Profiles linked to correct users")
