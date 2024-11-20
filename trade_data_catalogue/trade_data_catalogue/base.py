from django.views.generic import TemplateView

from .utils import get_breadcrumbs, get_transformed_string_from_pattern

class BaseBreadcrumbView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = get_breadcrumbs(self.request.path)
        return context


class DatasetVersionBreadcrumbView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dataset_id = kwargs.get("dataset_id")
        version = kwargs.get("version")
        context["breadcrumbs"] = self.dataset_version_breadcrumbs(dataset_id, version)
        return context
    
    def dataset_version_breadcrumbs(self, dataset_id, version):  
        breadcrumbs = [{ "name": "Dataset Catalogue", "url": "/"}]
        dataset_url = f"/{dataset_id}/{version}"
        breadcrumbs.append({ "name": self.get_formatted_dataset_breadcrumb_title(dataset_id), "url": dataset_url })
        return breadcrumbs
    
    def get_formatted_dataset_breadcrumb_title(self, dataset_id):
        dehyphenated_dataset_id = dataset_id.replace("-", " ")
        title_cased_dataset_id = dehyphenated_dataset_id.title()
        dataset_title_with_correct_region = get_transformed_string_from_pattern(
            title_cased_dataset_id, r"\b(Uk|Eu)\b"
        )

        return dataset_title_with_correct_region