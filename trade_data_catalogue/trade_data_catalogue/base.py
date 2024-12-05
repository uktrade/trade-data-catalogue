from django.views.generic import TemplateView

from .utils import (
    REGEX_PATTERNS,
    get_transformed_string_from_pattern,
    is_string_a_version,
    is_string_a_dataset_id,
)


class BaseBreadcrumbView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.request.path

        context["breadcrumbs"] = self.get_breadcrumbs(path)

        return context

    def get_breadcrumbs(self, path):
        breadcrumbs = [{"name": "Dataset Catalogue", "url": "/"}]
        segments = [segment for segment in path.strip("/").split("/") if segment]

        url = ""
        for segment in segments:
            url += f"/{segment}"

            if segment == "table" or segment == "report":
                continue

            breadcrumbs.append(
                {
                    "name": (
                        self.get_formatted_dataset_breadcrumb_title(segment)
                        if not is_string_a_version(segment)
                        else segment
                    ),
                    "url": url,
                    "is_dataset_id": is_string_a_dataset_id(segment),
                }
            )

        return breadcrumbs

    def get_formatted_dataset_breadcrumb_title(self, dataset_id):
        remove_dataset_id_text = dataset_id.replace("dataset-id", "")
        dehyphenated_dataset_id = remove_dataset_id_text.replace("-", " ").replace(
            ".", " "
        )
        title_cased_dataset_id = dehyphenated_dataset_id.title()

        for pattern in REGEX_PATTERNS.values():
            title_cased_dataset_id = get_transformed_string_from_pattern(
                title_cased_dataset_id, pattern
            )

        return title_cased_dataset_id
