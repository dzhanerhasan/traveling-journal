from django.forms import ModelForm

from finalProject.main.models import Picture, Album


class CreatePhotoForm(ModelForm):
    class Meta:
        model = Picture
        fields = [
            'album',
            'description',
            'photo',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreatePhotoForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['album'].queryset = Album.objects.filter(author=self.user)


class EditPhotoForm(ModelForm):
    class Meta:
        model = Picture
        fields = [
            'album',
            'description',
            'photo',
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['album'].queryset = Album.objects.filter(author=self.user)
