"""
Examinations app models.
"""
from django.db import models
from apps.patients.models import Patient
from apps.users.models import User


class Examination(models.Model):
    """Eye examination model for storing examination data."""
    
    VISUAL_ACUITY_CHOICES = [
        ('20/20', '20/20 (Normal)'),
        ('20/40', '20/40'),
        ('20/60', '20/60'),
        ('20/100', '20/100'),
        ('20/200', '20/200'),
        ('CF', 'Counting Fingers'),
        ('LP', 'Light Perception'),
        ('NLP', 'No Light Perception'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='examinations')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              limit_choices_to={'role': 'doctor'}, related_name='examinations_conducted')
    
    examination_date = models.DateTimeField(auto_now_add=True)
    
    # Visual acuity
    right_eye_va = models.CharField(max_length=20, choices=VISUAL_ACUITY_CHOICES, blank=True)
    left_eye_va = models.CharField(max_length=20, choices=VISUAL_ACUITY_CHOICES, blank=True)
    
    # Intraocular pressure
    right_eye_iop = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="mmHg")
    left_eye_iop = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="mmHg")
    
    # Refraction
    right_eye_sphere = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_eye_cylinder = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    right_eye_axis = models.IntegerField(null=True, blank=True)
    
    left_eye_sphere = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_eye_cylinder = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    left_eye_axis = models.IntegerField(null=True, blank=True)
    
    # Clinical findings
    external_findings = models.TextField(blank=True)
    anterior_segment = models.TextField(blank=True)
    posterior_segment = models.TextField(blank=True)
    
    # Diagnosis and recommendations
    diagnosis = models.TextField()
    recommendations = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Examination'
        verbose_name_plural = 'Examinations'
        ordering = ['-examination_date']

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.examination_date.strftime('%Y-%m-%d')}"
