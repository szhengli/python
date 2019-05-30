from django.db import models

class Publiser(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

        # test

    def __str__(self):
        return self.name

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publiser, on_delete=models.CASCADE)
    publication_date = models.DateField()

class Backends(models.Model):
    folder = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100)

class FrontEnds(models.Model):
    folder = models.CharField(max_length=100)

class Deploy_Records(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)
    source = models.CharField(max_length=100,default="")
    target = models.CharField(max_length=100,default="")
    items = models.CharField(max_length=100)





























class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes =  models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class ComonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField

    class Meta:
        abstract = True


class Student(ComonInfo):
    home_group = models.CharField(max_length=5)


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()





