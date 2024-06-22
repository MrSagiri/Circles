from django import forms
from .models import newAcc, Posts
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class newAccForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = newAcc
        # fields = "__all__"
        fields = ['birthday', 'bio', 'image', 'sex', 'address']
        labels = {
            # 'firstname' : 'First Name',
            # 'lastname' : 'Last Name',
            'birthday':'Date of Birth',
            'bio':'Add a Bio to your Profile',
            'image' : 'Profile Picture',
            # 'username': 'Username',
            # 'password': 'Password',
            # 'password2': 'Confirm Password'
        }
        # firstname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # lastname = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(newAccForm, self).__init__(*args, **kwargs)

        self.fields['birthday'].widget.attrs.update({
            'style': 'width: 100%'
        })

        self.fields['image'].widget.attrs.update({
            'id':'update',
            'style':'display:none'
        })
        
    def clean_photo(self):
        image = self.cleaned_data.get('image')
        # Perform custom validation if needed
        if not image:
            print(forms.ValidationError("Image is required"))
            raise forms.ValidationError("Image is required")
        if image.size > 5*1024*1024:
            print(forms.ValidationError("Image file too large ( > 5MB )"))
            raise forms.ValidationError("Image file too large ( > 5MB )")
            
        return image

    def save(self, commit=True):
        instance = super().save(commit=False)
        # instance.image = '/User Pics/' + self.cleaned_data['image'].name
        instance.image = self.cleaned_data['image']
        instance.bio = self.cleaned_data['bio']
        instance.birthday = self.cleaned_data['birthday']
        if commit:
            instance.save()
        return instance

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", required=True, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class PostsForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ['content']
    content = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class': 'yo px-3 py-2 border-2 border-black rounded-md focus:outline-none focus:border-red-600', 'rows': 4}))

class CreateForm(UserCreationForm):
    first_name = forms.CharField(label="First Name",required=True, max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control'}) )
    username = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", required=True, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Password confirmation", required=True, strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username already in use.')
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set the hashed password
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user