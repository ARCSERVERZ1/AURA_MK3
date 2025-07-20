from django.db import models


# Create your models here.

class medtrac_log(models.Model):
    id = models.IntegerField(primary_key=True)
    participant = models.CharField(max_length=200)
    recorder = models.CharField(max_length=200)
    test_parameter = models.CharField(max_length=200)
    v1 = models.CharField(max_length=200)
    v2 = models.CharField(max_length=200)
    v3 = models.CharField(max_length=200)
    date = models.DateField()
    time_stamp = models.DateTimeField()
    remarks = models.CharField(max_length=200)
    updated_by = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-' + str(self.test_parameter) + '-' + str(self.date)


class food_log(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=200)
    food_type = models.CharField(max_length=200)
    food_qty = models.CharField(max_length=200)
    satisfaction_level = models.CharField(max_length=200)
    junk_rating = models.CharField(max_length=200)
    date = models.DateField()
    time_stamp = models.DateTimeField()
    food_description = models.CharField(max_length=200)
    updated_by = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-' + str(self.food_type) + '-' + str(self.date)

class MealDataLog(models.Model):
    FOOD_TYPE_CHOICES = [
        ('Veg', 'Vegetarian'),
        ('Non-Veg', 'Non-Vegetarian'),
        ('Egg', 'Egg'),
        ('other', 'Other'),
        ('Tiffin', 'Tiffin'),
    ]

    FOOD_CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
        ('other', 'Other'),
    ]

    id = models.AutoField(primary_key=True)  # AutoField is recommended for primary key
    user = models.CharField(max_length=200, verbose_name="User Name")
    food_qty = models.CharField(max_length=200, verbose_name="Quantity")
    food_description = models.TextField(verbose_name="Description", blank=True)
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES)
    food_category = models.CharField(max_length=20, choices=FOOD_CATEGORY_CHOICES)
    spare = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    time_stamp = models.DateTimeField()
    updated_by = models.CharField(max_length=200, verbose_name="Updated By")

    class Meta:
        verbose_name = "Meal Data Log"
        verbose_name_plural = "Meal Data Logs"
        ordering = ['-date', '-time_stamp']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['date']),
            models.Index(fields=['food_type']),
        ]

    def __str__(self):
        return f"{self.id} - {self.food_type} - {self.date}"


class HealthIncidentLogs(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=200)
    discomfort = models.CharField(max_length=200)
    severity = models.CharField(max_length=200)
    apprx_start_time = models.DateTimeField()
    apprx_end_time = models.DateTimeField()
    medication = models.CharField(max_length=200)
    while_remarks = models.TextField()
    after_remarks = models.TextField()
    time_stamp = models.DateTimeField()
    updated_by = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-' + str(self.discomfort) + '-' + str(self.severity)


class config_discomfort(models.Model):
    id = models.IntegerField(primary_key=True)
    discomfort_id = models.CharField(max_length=200)
    discomfort = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + '-' + str(self.discomfort_id) + '-' + str(self.discomfort)
