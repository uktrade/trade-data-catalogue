from django.views.generic import TemplateView

from .utils import get_transformed_string_from_pattern, is_string_a_version


class BaseBreadcrumbView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = self.request.path

        context["breadcrumbs"] = self.get_breadcrumbs(path)

        return context

    def get_breadcrumbs(self, path):
        breadcrumbs = [{"name": "Dataset Catalogue", "url": "/"}]
        segments = [segment for segment in path.strip("/").split("/") if segment]

        print(segments)

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
                }
            )

        print(breadcrumbs)

        return breadcrumbs

    def get_formatted_dataset_breadcrumb_title(self, dataset_id):
        dehyphenated_dataset_id = dataset_id.replace("-", " ")
        title_cased_dataset_id = dehyphenated_dataset_id.title()
        dataset_title_with_correct_region = get_transformed_string_from_pattern(
            title_cased_dataset_id, r"\b(Uk|Eu)\b"
        )

        return dataset_title_with_correct_region
