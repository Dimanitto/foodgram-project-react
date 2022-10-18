import csv
from django.db.models import QuerySet
from django.http import HttpResponse


class ReportCsv:
    def __init__(self, qs: QuerySet, columns, user) -> None:
        super().__init__()
        self.qs = qs
        self.fields = columns
        self.user = user

    def generate_csv(self, writer: csv.writer) -> None:
        # Запишем названия для колонок
        writer.writerow(self.fields)

        output = []
        for obj in self.qs:
            output.append(
                [
                    obj.get('recipe__ingredientamounts__ingredient__name'),
                    obj.get('sum'),
                    obj.get('recipe__ingredientamounts__ingredient__measurement_unit')
                ]
            )
        writer.writerows(output)

    def get_http_response(self) -> HttpResponse:
        """Создание и отдача .csv отчета."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Shopping cart - {self.user}.csv"'

        writer = csv.writer(response)
        self.generate_csv(writer)
        return response
