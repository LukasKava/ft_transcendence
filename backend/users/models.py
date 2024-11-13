from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_file_size

AUTH_PROVIDERS ={'email': 'email', '42api': '42api'}

class User(AbstractUser):
    email = models.EmailField(unique=True)
    auth_provider=models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(
        default='avatar.png',
        null=True, blank=True,
        validators=[validate_file_size]
    )
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    friends = models.ManyToManyField("self", blank=True)
    online_status = models.BooleanField(default=False)
    matches = models.ManyToManyField(
        'Match', through='PlayerMatch', related_name='stats', blank=True)

    def __str__(self):
        return self.display_name

    def __str__(self):
        return self.user.email  # This will display the email in the profile


class Match(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    player1 = models.ForeignKey(
        PlayerProfile, related_name='player1_matches',
        on_delete=models.CASCADE)
    player2 = models.ForeignKey(
        PlayerProfile, related_name='player2_matches',
        on_delete=models.CASCADE)
    winner = models.ForeignKey(
        PlayerProfile, related_name='won_matches', on_delete=models.CASCADE)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()

    def __str__(self):
        return f'{self.player1.display_name} vs {self.player2.display_name}\
                on {self.date}'


class PlayerMatch(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} played in match {self.match} on {self.date}"