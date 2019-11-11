from django import forms


class CommentsForm(forms.Form):
    author = forms.CharField(max_length=50, 
    		widget=forms.TextInput(attrs={
    			"class":"form-control",
    			"placeholder":"Enter your name"}))

    body  	= forms.CharField(
    		widget=forms.Textarea(attrs={
    			"class":"form-control",
    			"placeholder":"Leave your comment"}))