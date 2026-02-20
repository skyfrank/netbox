from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from dcim.models import Site, Location
from utilities.forms.fields import DynamicModelChoiceField


__all__ = ("NameBuilderForm",)


class NameBuilderForm(forms.Form):
    """
    A form to build device names based on site and location selections.
    """

    def __init__(self, *args, **kwargs):
        from netbox_custom_objects.models import CustomObjectType

        super().__init__(*args, **kwargs)

        config = settings.PLUGINS_CONFIG.get("custom_object_types_name", {})

        system_name = config.get("system", "systeme")
        subsystem_name = config.get("subsystem", "sous_systeme")
        component_name = config.get("component", "composant")

        system = CustomObjectType.objects.get(name=system_name).get_model()
        subsystem = CustomObjectType.objects.get(name=subsystem_name).get_model()
        component = CustomObjectType.objects.get(name=component_name).get_model()

        self.fields["nb_system"] = DynamicModelChoiceField(
            queryset=system.objects.all(),
            label=_("System"),
            help_text=_("System"),
            required=False,
        )
        self.fields["nb_subsystem"] = DynamicModelChoiceField(
            queryset=subsystem.objects.all(),
            label=_("Subsystem"),
            help_text=_("Subystem"),
            query_params={system_name: "$nb_system"},
            required=False,
        )
        self.fields["nb_component"] = DynamicModelChoiceField(
            queryset=component.objects.all(),
            label=_("Component"),
            help_text=_("Component"),
            query_params={
                system_name: "$nb_system",
                subsystem_name: "$nb_subsystem",
            },
            required=False,
        )

    nb_site = DynamicModelChoiceField(
        label=_("Site"),
        queryset=Site.objects.all(),
        required=False,
    )
    nb_location = DynamicModelChoiceField(
        label=_("Location"),
        queryset=Location.objects.all(),
        query_params={"site_id": "$nb_site"},
        required=False,
    )
    nb_system = forms.HiddenInput()
    nb_subsystem = forms.HiddenInput()
    nb_component = forms.HiddenInput()
    nb_instance = forms.CharField(
        label=_("Name"),
        required=False,
    )
    nb_name = forms.CharField(
        label=_("Full Name"),
    )
