import json

from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Member
from ..serializers import MemberSerializer

# initialize the APIClient app
client = Client()


class GetAllMembersTest(TestCase):
    """ Test module for GET all members API """

    def setUp(self):
        user = User.objects.create(first_name='user', last_name='test', password='p@ssw0rD1',
                                   username='test_user', email='test_user@test.com')
        Member.objects.create(
            first_name='jollibee', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)
        Member.objects.create(
            first_name='mcdo', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)

    def test_get_all_member(self):
        # get API response
        response = client.get(reverse('get_post_member'))
        # get data from db
        member = Member.objects.all()
        serializer = MemberSerializer(member, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleMemberTest(TestCase):
    def setUp(self):
        user = User.objects.create(first_name='user', last_name='test', password='p@ssw0rD1',
                                   username='test_user', email='test_user@test.com')
        self.jollibee = Member.objects.create(
            first_name='jollibee', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)
        self.mcdo = Member.objects.create(
            first_name='mcdo', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)

    def test_get_valid_single_member(self):
        response = client.get(reverse('get_delete_update_member', kwargs={'pk': self.jollibee.pk}))
        member = Member.objects.get(pk=self.jollibee.pk)
        serializer = MemberSerializer(member)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_member(self):
        response = client.get(
            reverse('get_delete_update_member', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewMemberTest(TestCase):
    """ Test module for inserting a new member """

    def setUp(self):
        user = User.objects.create(first_name='user', last_name='test', password='p@ssw0rD1',
                                   username='test_user', email='test_user@test.com')

        self.valid_payload = {
            "first_name": "test first",
            "last_name": "test last",
            "vital_status": "ded",
            "relationship": "uncle",
            "dob": "1998-01-01",
            "generation_level": 2,
            "user": user.id
        }

        self.invalid_payload = {
            'first_name': '',
            'last_name': 'test last',
            'vital_status': 'ded',
            'relationship': 'uncle',
            'dob': '1998-01-01',
            'generation_level': 1,
            "user": user.id
        }

    def test_create_valid_member(self):
        response = client.post(
            reverse('get_post_member'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_member(self):
        response = client.post(
            reverse('get_post_member'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleMemberTest(TestCase):
    """ Test module for updating an existing member record """

    def setUp(self):
        user = User.objects.create(first_name='user', last_name='test', password='p@ssw0rD1',
                                   username='test_user', email='test_user@test.com')
        self.jollibee = Member.objects.create(
            first_name='jollibee', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)
        self.mcdo = Member.objects.create(
            first_name='mcdo', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)

        self.valid_payload = {
            "first_name": "jollibee",
            "last_name": "no last",
            "vital_status": "no last",
            "relationship": "uncle",
            "dob": "1998-01-01",
            "generation_level": 1,
            "user": user.id
        }

        self.invalid_payload = {
            "first_name": "",
            "last_name": "no last",
            "vital_status": "no last",
            "relationship": "uncle",
            "dob": "1998-01-01",
            "generation_level": 1,
            "user": user.id
        }

    def test_valid_update_member(self):
        response = client.put(
            reverse('get_delete_update_member', kwargs={'pk': self.jollibee.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_member(self):
        response = client.put(
            reverse('get_delete_update_member', kwargs={'pk': self.jollibee.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleMemberTest(TestCase):
    """ Test module for deleting an existing puppy member """

    def setUp(self):
        user = User.objects.create(first_name='user', last_name='test', password='p@ssw0rD1',
                                   username='test_user', email='test_user@test.com')
        self.jollibee = Member.objects.create(
            first_name='jollibee', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)
        self.mcdo = Member.objects.create(
            first_name='mcdo', last_name='no last', vital_status='no last', relationship='uncle',
            dob='1998-01-01', generation_level=1, user_id=user.id)

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_member', kwargs={'pk': self.jollibee.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('get_delete_update_member', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)