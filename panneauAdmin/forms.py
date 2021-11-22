from django import forms

class SupprimerIDForm(forms.Form):
    liste_identifiants = forms.CharField(label="",
    widget=forms.TextInput(attrs={'placeholder': 'Entrez les numéros à supprimer : '}))
    confirmation = forms.CheckboxInput()
class ConnexionForm(forms.Form):
    pseudo = forms.CharField(label="Pseudo",
    widget=forms.TextInput(attrs={'placeholder': 'Entrez votre pseudo'}))
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={"id" : "mot_de_passe", "placeholder" : "Entrez votre mot de passe"}),
        label="Mot de passe",
    )

    """def clean(self):
        pseudo = self.cleaned_data.get("pseudo")
        mot_de_passe = self.cleaned_data.get("mot_de_passe")"""

    def clean_username(self):
        pseudo = self.cleaned_data.get("username")
        qs = User.objects.filter(pseudo__iexact=pseudo)

        if not qs.exists():
            raise forms.ValidationError("Ce nom d'utilisateur est invalide!")
        
        return pseudo
class CommandeForm(forms.Form):
    liste_identifiants = forms.CharField(label="",
    widget=forms.TextInput(attrs={'placeholder': 'Entrez la commande pour le serveur : '}))
