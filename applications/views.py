from django.urls import reverse_lazy

from editor.base_views import (
    ApiClientTemplateView,
    ColumnMetadataApiClientMixin,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
)
from editor.views import (
    EditorOverviewTemplateView,
    EditorProcessFormView,
    EditorStartFormView,
)
from resource_management.views import ResourceListContextMixin, ResourceListFormView

from .api.api_clients import (
    ApplicationApiClient,
    ApplicationColumnMetadataApiClient,
)
from .forms import ApplicationEditorForm, ApplicationRegistrationForm


class ApplicationViewMixin(
    ApiClientTemplateView,
    ColumnMetadataApiClientMixin,
    EditorContextMixin,
    ResourceTypeNameContextMixin,
    ResourceListContextMixin,
):
    api_client_class = ApplicationApiClient
    editor_url_reverse_base = "applications:application_editor"
    editor_start_url_reverse_base = "applications:new_application"
    editor_overview_url_reverse_base = "applications:application_overview"
    column_metadata_api_client_class = ApplicationColumnMetadataApiClient
    resource_type_name_singular = "application"
    resource_type_name_plural = "applications"
    editor_resource_list_url_reverse = "applications:application_list"


class ApplicationEditorStartFormView(EditorStartFormView, ApplicationViewMixin):
    template_name = "applications/new_application_start.html"
    form_class = ApplicationRegistrationForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationEditorProcessFormView(EditorProcessFormView, ApplicationViewMixin):
    template_name = "applications/application_editor.html"
    main_form_class = ApplicationEditorForm
    success_url = reverse_lazy("applications:new_application")


class ApplicationListFormView(ResourceListFormView, ApplicationViewMixin):
    template_name = "applications/applications.html"
    new_resource_reverse = "applications:new_application"


class ApplicationEditorOverviewTemplateView(
    EditorOverviewTemplateView, ApplicationViewMixin
):
    template_name = "applications/application_overview.html"
