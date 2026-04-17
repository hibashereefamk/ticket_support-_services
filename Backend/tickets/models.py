from django.db import models
category_choices = [
    ('technical', 'Technical'),
    ('billing', 'Billing'),
    ('general', 'General'),
]
priority_choices = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]
choice_status = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('closed', 'Closed'),
    ('resolved', 'Resolved'),
]
class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category =models.CharField(choices=category_choices, max_length=20)
    priority = models.CharField(choices=priority_choices, max_length=10)
    status = models.CharField(max_length=20, default='open', choices=choice_status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
