from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    class GestureActions(models.IntegerChoices):
        OnlyIndexFingerUp = 1, 'Only Index finger Up'
        IndexAndMiddleFingersUp = 2, 'Index and middle finger up'
        IndexAndThumbFinger = 3, 'Index and thumb finger'
        RingFingerUp = 4, 'Ring finger up'
        IndexAndLastFingerUp = 5, 'Index and last finger up'
        AllFingersUp = 6, 'All fingers up'
        AllFingersDown = 7, 'All fingers closed'

    name = models.CharField(max_length=100, null=True, blank=True)
    category_id = models.IntegerField(choices=GestureActions.choices)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class mouseAction(models.Model):
    class Category(models.IntegerChoices):
        CURSOR_MOVEMENT = 1, 'Cursor Movement'
        MOUSE_LEFT_CLICK = 2, 'Mouse Left Click'
        MOUSE_RIGHT_CLICK = 3, 'Mouse Right Click'
        SCREENSHOT = 4, 'ScreenShot'
        ZOOM_ACTIONS = 5, 'Zoom In and Zoom Out'
        CLEAR = 6, 'Clear'

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    gesture_category = models.ManyToManyField(category, blank=True, related_name="mouse_actions") # This is to specify which all gestures can be choosen by the user for this mouse action.
    category_id = models.IntegerField(choices=Category.choices)
    gif_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class category_MouseAction_Mapping(models.Model):
    category = models.ForeignKey(category, related_name = "mappings", on_delete=models.CASCADE)
    mouse_action = models.ForeignKey(mouseAction, related_name = "mappings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = "mappings", on_delete=models.CASCADE)

    @classmethod
    def create_update_mapping(cls, category_instance, mouse_action_instance, user_instance):
        try:
            existing_mapping = cls.objects.get(mouse_action=mouse_action_instance, user=user_instance)

            existing_mapping.category = category_instance
            existing_mapping.save()
            return existing_mapping

        except cls.DoesNotExist:
            new_mapping = cls(category=category_instance, mouse_action=mouse_action_instance, user=user_instance)
            new_mapping.save()
            return new_mapping

    @classmethod
    def get_mapping(cls, mouse_action, user):
        try:
            mapping = cls.objects.get(mouse_action=mouse_action, user=user)
            return mapping
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_all_gestures(cls, user):
        try:
            mappings = cls.objects.filter(user=user)
            gesture = []
            for mapping in mappings:
                gesture.append(mapping.category.id)
            return gesture
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_all_actions(cls, user):
        try:
            mappings = cls.objects.filter(user=user)
            actions = []
            for mapping in mappings:
                actions.append(mapping.mouse_action.id)
            return actions
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_mapping_using_gesture(cls, gesture, user):
        try:
            mapping = cls.objects.get(category=gesture, user=user)
            return mapping
        except cls.DoesNotExist:
            return False
