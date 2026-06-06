"""
Appointments app models.
"""
from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.patients.models import Patient


class Appointment(models.Model):
    """Appointment model for scheduling patient visits."""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('surgery', 'Surgery'),
        ('diagnostic', 'Diagnostic Test'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                              limit_choices_to={'role': 'doctor'}, related_name='appointments_as_doctor')
    
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    reason_for_visit = models.TextField()
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_upcoming(self):
        return self.appointment_date > timezone.now() and self.status == 'scheduled'
