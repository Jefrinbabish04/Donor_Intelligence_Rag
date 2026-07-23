from django.db import models

# Create your models here.
class Donor(models.Model):
    donor_id = models.CharField(
        max_length=50, 
        unique=True,
        db_index=True,
        )
    
    name = models.CharField(
        max_length=150,
        db_index=True,
        )
    age = models.PositiveBigIntegerField()

    gender = models.CharField(
        max_length=20,
        db_index=True,
        )
    
    blood_group = models.CharField(
        max_length=10,
        db_index=True,
        )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        db_index=True,
    )

    state = models.CharField(
        max_length=100,
        db_index=True,
    )

    country = models.CharField(
        max_length=100,
        default="India",
        db_index=True,
    )

    medical_history = models.TextField(
        blank=True,
    )

    last_donation_date = models.DateField(
        null=True,
        blank=True,
    )

    eligible_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    donation_count = models.PositiveIntegerField(
        default=0,
    )

    notes = models.TextField(
        blank=True,
    )

    hospital = models.CharField(
        max_length=200,
        blank=True,
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    tags = models.JSONField(
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.donor_id} - {self.name}"