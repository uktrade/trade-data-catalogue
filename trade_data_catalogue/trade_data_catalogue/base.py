from django.views.generic import TemplateView

from .utils import get_breadcrumbs

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
        breadcrumbs.append({ "name": dataset_id, "url": dataset_url })
        return breadcrumbs