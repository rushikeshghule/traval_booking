# Generated by Django 5.2 on 2025-04-14 12:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Airline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=10, unique=True)),
                (
                    "logo",
                    models.ImageField(blank=True, null=True, upload_to="airlines"),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("website", models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Airport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=10, unique=True)),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Flight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flight_number", models.CharField(max_length=20)),
                ("departure_time", models.DateTimeField()),
                ("arrival_time", models.DateTimeField()),
                ("duration", models.DurationField(blank=True, null=True)),
                (
                    "flight_type",
                    models.CharField(
                        choices=[
                            ("domestic", "Domestic"),
                            ("international", "International"),
                        ],
                        max_length=20,
                    ),
                ),
                ("base_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("available_seats", models.PositiveIntegerField()),
                (
                    "aircraft_type",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "airline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="flights",
                        to="flight.airline",
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="arrivals",
                        to="flight.airport",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="departures",
                        to="flight.airport",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FlightSeat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("seat_number", models.CharField(max_length=10)),
                (
                    "seat_class",
                    models.CharField(
                        choices=[
                            ("economy", "Economy"),
                            ("premium_economy", "Premium Economy"),
                            ("business", "Business"),
                            ("first", "First Class"),
                        ],
                        max_length=20,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("available", "Available"),
                            ("booked", "Booked"),
                            ("reserved", "Reserved"),
                            ("unavailable", "Unavailable"),
                        ],
                        default="available",
                        max_length=20,
                    ),
                ),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seats",
                        to="flight.flight",
                    ),
                ),
            ],
            options={
                "unique_together": {("flight", "seat_number")},
            },
        ),
        migrations.CreateModel(
            name="FlightBooking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booking_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("cancelled", "Cancelled"),
                            ("completed", "Completed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("paid", "Paid"),
                            ("refunded", "Refunded"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("booking_reference", models.CharField(max_length=20, unique=True)),
                ("passenger_count", models.PositiveIntegerField()),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="flight.flight",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_bookings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "seats",
                    models.ManyToManyField(
                        related_name="bookings", to="flight.flightseat"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Passenger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "passport_number",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("date_of_birth", models.DateField()),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="passengers",
                        to="flight.flightbooking",
                    ),
                ),
            ],
        ),
    ]
